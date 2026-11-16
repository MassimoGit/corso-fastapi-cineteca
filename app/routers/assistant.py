"""L'assistente: la risposta in streaming."""
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.services import assistant as assistant_service

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.get("/stream")
def stream_answer(
    question: Annotated[str, Query(min_length=1, max_length=200)], delay_s: Annotated[float, Query(ge=0, le=2)] = 0.3
) -> StreamingResponse:
    """La risposta del finto modello, una parola alla volta. La route è def: costruisce solo la risposta, il generatore è async."""
    return StreamingResponse(assistant_service.fake_model(question, delay_s), media_type="text/plain; charset=utf-8")
