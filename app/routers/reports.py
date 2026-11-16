"""I report: risposte lunghe che arrivano a pezzi."""
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.dependencies import SessionDep
from app.services import reports as reports_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/screenings")
def screenings_report(
    session: SessionDep, pause_s: Annotated[float, Query(ge=0, le=2)] = 0
) -> StreamingResponse:
    """Il report delle proiezioni: una riga di testo per volta. pause_s serve a vederlo arrivare a pezzi."""
    rows = reports_service.list_screening_rows(session)  # la lettura finisce qui: il generatore non usa la Session
    return StreamingResponse(reports_service.report_lines(rows, pause_s), media_type="text/plain; charset=utf-8")
