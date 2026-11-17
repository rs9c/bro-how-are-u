from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services import logger
from app.services.stream import hub

router = APIRouter(tags=["stream"])


@router.websocket("/stream/ws")
async def stream_ws(websocket: WebSocket):
    """
    视频流WebSocket
    """
    queue = hub.subscribe()
    try:
        await hub.wait_ready()
        await websocket.accept()
        logger.info("WebSocket已连接")
        while True:
            payload = await queue.get()
            if payload is None:
                break
            await websocket.send_bytes(payload)
    except WebSocketDisconnect:
        logger.info("WebSocket断开连接")
    finally:
        await hub.unsubscribe(queue)
