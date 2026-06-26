from pydantic import BaseModel, Field

from app.models.enums import CaseType, Department, Severity


class SortTicketResponse(BaseModel):
    ticket_id: str
    case_type: CaseType
    severity: Severity
    department: Department
    agent_summary: str = Field(..., min_length=1)
    human_review_required: bool
    confidence: float = Field(..., ge=0.0, le=1.0)


class HealthResponse(BaseModel):
    status: str = "ok"
