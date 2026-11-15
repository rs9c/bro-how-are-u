import asyncio
import json

import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services import config, detect, logger

router = APIRouter(tags=["stream"])


@router.websocket("/stream/ws")
async def stream_ws(websocket: WebSocket):
    """
    视频流WebSocket
    """
    streamCfg = config.cfg["stream"]
    logger.info("读取到stream配置：" + json.dumps(streamCfg))
    await websocket.accept()
    cap = cv2.VideoCapture(streamCfg["camera"])
    max_fps: float = streamCfg["max_fps"]
    jpg_quality: int = streamCfg["jpg_quality"]
    interval = 1.0 / max_fps
    try:
        retry = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                if retry >= 100:
                    logger.error("无法读取帧，终止循环")
                    break
                retry += 1
                logger.warn("无法读取帧，重试：" + str(retry))
                await asyncio.sleep(interval)
                continue
            retry = 0
            annotated = detect.detect(frame)
            ret, buffer = cv2.imencode(
                ".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, jpg_quality]
            )
            if not ret:
                logger.warn("编码失败，跳过本帧")
                continue
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(interval)
    except WebSocketDisconnect:
        logger.info("WebSocket断开连接")
    finally:
        cap.release()
