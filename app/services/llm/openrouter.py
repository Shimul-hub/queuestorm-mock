import json
import logging

import httpx

from app.core.config import Settings
from app.models.enums import CaseType, Department, Severity
from app.schemas.request import SortTicketRequest
from app.services.llm.base import AIReasoner, LLMClassification

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You classify customer support tickets for a digital finance company.
Return ONLY valid JSON with these exact fields and enum values:
{
  "case_type": "wrong_transfer|payment_failed|refund_request|phishing_or_social_engineering|other",
  "severity": "low|medium|high|critical",
  "department": "customer_support|dispute_resolution|payments_ops|fraud_risk",
  "agent_summary": "one neutral English sentence for a support agent",
  "human_review_required": true|false,
  "confidence": 0.0-1.0
}
Rules:
- human_review_required must be true for phishing_or_social_engineering or critical severity
- Never ask for PIN, OTP, password, or card number in agent_summary
- Never promise refunds, approvals, or account actions
- Use evidence from the customer message only
"""


class OpenRouterReasoner(AIReasoner):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._base_url = "https://openrouter.ai/api/v1/chat/completions"

    async def classify(
        self, request: SortTicketRequest, script_profile: str
    ) -> LLMClassification | None:
        if not self._settings.llm_available:
            return None

        locale_hint = request.locale.value if request.locale else script_profile
        user_prompt = (
            f"ticket_id={request.ticket_id}\n"
            f"locale={locale_hint}\n"
            f"channel={request.channel.value if request.channel else 'unknown'}\n"
            f"message={request.message}\n"
            "Classify this ticket."
        )

        payload = {
            "model": self._settings.openrouter_model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 256,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self._settings.openrouter_api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self._settings.llm_timeout_seconds) as client:
                response = await client.post(self._base_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                result = LLMClassification.model_validate(parsed)
                return _enforce_policy(result)
        except Exception as exc:
            logger.warning("OpenRouter classification failed: %s", type(exc).__name__)
            return None


def _enforce_policy(result: LLMClassification) -> LLMClassification:
    updates: dict[str, object] = {}

    if result.case_type == CaseType.PHISHING:
        updates["severity"] = Severity.CRITICAL
        updates["human_review_required"] = True
        updates["department"] = Department.FRAUD_RISK
    elif result.severity == Severity.CRITICAL:
        updates["human_review_required"] = True

    if result.case_type == CaseType.WRONG_TRANSFER:
        updates["department"] = Department.DISPUTE_RESOLUTION
    elif result.case_type == CaseType.PAYMENT_FAILED:
        updates["department"] = Department.PAYMENTS_OPS

    if updates:
        return result.model_copy(update=updates)
    return result
