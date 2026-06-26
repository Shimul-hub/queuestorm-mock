from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from app.models.enums import CaseType, Department, Severity
from app.schemas.request import SortTicketRequest


class LLMClassification(BaseModel):
    case_type: CaseType
    severity: Severity
    department: Department
    agent_summary: str = Field(..., min_length=1)
    human_review_required: bool
    confidence: float = Field(..., ge=0.0, le=1.0)


class AIReasoner(ABC):
    @abstractmethod
    async def classify(
        self, request: SortTicketRequest, script_profile: str
    ) -> LLMClassification | None:
        raise NotImplementedError
