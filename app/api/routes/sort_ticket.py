from fastapi import APIRouter, Depends

from app.api.dependencies import get_cached_settings
from app.core.config import Settings
from app.schemas.request import SortTicketRequest
from app.schemas.response import SortTicketResponse
from app.services.ticket_service import TicketService

router = APIRouter(tags=["tickets"])


def get_ticket_service(settings: Settings = Depends(get_cached_settings)) -> TicketService:
    return TicketService(settings)


@router.post("/sort-ticket", response_model=SortTicketResponse)
async def sort_ticket(
    payload: SortTicketRequest,
    service: TicketService = Depends(get_ticket_service),
) -> SortTicketResponse:
    return await service.classify(payload)
