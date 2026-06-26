from app.core.config import Settings
from app.models.enums import CaseType
from app.schemas.request import SortTicketRequest
from app.schemas.response import SortTicketResponse
from app.services.classifier.human_review import requires_human_review
from app.services.classifier.pipeline import ClassificationResult, classify_message
from app.services.llm.openrouter import OpenRouterReasoner
from app.services.summary.generator import generate_summary
from app.validators.safety import is_summary_safe, sanitize_summary


class TicketService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._llm = OpenRouterReasoner(settings)

    async def classify(self, request: SortTicketRequest) -> SortTicketResponse:
        rule_result = classify_message(request.message)

        if (
            self._settings.llm_available
            and rule_result.confidence < self._settings.llm_confidence_threshold
        ):
            llm_result = await self._llm.classify(
                request, script_profile=rule_result.script_profile
            )
            if llm_result is not None:
                summary = sanitize_summary(llm_result.agent_summary)
                if not is_summary_safe(summary):
                    summary = sanitize_summary(
                        generate_summary(
                            llm_result.case_type, request.message, rule_result.normalized_text
                        )
                    )
                return SortTicketResponse(
                    ticket_id=request.ticket_id,
                    case_type=llm_result.case_type,
                    severity=llm_result.severity,
                    department=llm_result.department,
                    agent_summary=summary,
                    human_review_required=llm_result.human_review_required,
                    confidence=round(llm_result.confidence, 2),
                )

        return self._from_rule_result(request.ticket_id, request.message, rule_result)

    def _from_rule_result(
        self, ticket_id: str, raw_message: str, result: ClassificationResult
    ) -> SortTicketResponse:
        summary = sanitize_summary(
            generate_summary(result.case_type, raw_message, result.normalized_text)
        )
        human_review = requires_human_review(result.case_type, result.severity)
        if result.case_type == CaseType.PHISHING:
            human_review = True

        return SortTicketResponse(
            ticket_id=ticket_id,
            case_type=result.case_type,
            severity=result.severity,
            department=result.department,
            agent_summary=summary,
            human_review_required=human_review,
            confidence=result.confidence,
        )
