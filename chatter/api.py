import asyncio

from typing import List, Annotated, Tuple
from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from common.callbacks.stream_handler import StreamingCallbackHandler
from chatter.chatter import Chatter


def register_chatter_api(chatter: Chatter) -> APIRouter:
    router = APIRouter(prefix="/api/chatter", tags=["Gonswap Chatter API Endpoints"])

    @router.post("/chat")
    async def chat(
        question: Annotated[str, Body()],
        chat_history: List[Tuple[str, str]],
    ):
        stream_handler = StreamingCallbackHandler()

        async def _chatting():
            try:
                await chatter.chat(
                    question,
                    chat_history,
                    stream_handler=stream_handler,
                )
                # await stream_handler.send_metadata(answer)
            except Exception as e:
                await stream_handler.send_error(repr(e))
            finally:
                await stream_handler.stop()

        asyncio.create_task(_chatting())
        return StreamingResponse(
            stream_handler,
            media_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
            }
        )

    return router
