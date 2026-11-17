import asyncio
import json
import threading
import time

import cv2
import numpy as np

from app.services import config, detect, logger


class FrameReader:
    def __init__(self, streamCfg: dict, retryDelay: float) -> None:
        self._retryDelay = retryDelay
        self._cap = cv2.VideoCapture(streamCfg["camera"], cv2.CAP_MSMF)
        if self._cap.isOpened():
            self._cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        else:
            self._cap.release()
            self._cap = cv2.VideoCapture(streamCfg["camera"])
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, streamCfg["width"])
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, streamCfg["height"])
        self._lock = threading.Lock()
        self._frame: np.ndarray | None = None
        self._seq = 0
        self._running = True
        self.failed = False
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _loop(self) -> None:
        retry = 0
        while self._running:
            ok, frame = self._cap.read()
            if not ok:
                if retry >= 100:
                    logger.error("无法读取帧，终止循环")
                    self.failed = True
                    return
                retry += 1
                logger.warn("无法读取帧，重试：" + str(retry))
                time.sleep(self._retryDelay)
                continue
            retry = 0
            with self._lock:
                self._frame = frame
                self._seq += 1

    def read(self) -> tuple[int, np.ndarray | None]:
        with self._lock:
            return self._seq, self._frame

    def close(self) -> None:
        self._running = False
        self._thread.join(timeout=2)
        self._cap.release()


class StreamHub:
    def __init__(self) -> None:
        self._queues: set[asyncio.Queue] = set()
        self._task: asyncio.Task | None = None
        self._ready: asyncio.Event | None = None

    def subscribe(self) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=1)
        self._queues.add(queue)
        if self._task is None or self._task.done():
            self._ready = asyncio.Event()
            self._task = asyncio.create_task(self._run(self._ready))
        return queue

    async def wait_ready(self) -> None:
        if self._ready is not None:
            await self._ready.wait()

    async def unsubscribe(self, queue: asyncio.Queue) -> None:
        self._queues.discard(queue)
        if self._queues or self._task is None:
            return
        task, self._task = self._task, None
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

    def _publish(self, payload: bytes | None) -> None:
        for queue in self._queues:
            if queue.full():
                queue.get_nowait()
            queue.put_nowait(payload)

    async def _run(self, ready: asyncio.Event) -> None:
        streamCfg = config.cfg["stream"]
        logger.info("读取到stream配置：" + json.dumps(streamCfg))
        max_fps: float = streamCfg["max_fps"]
        jpg_quality: int = streamCfg["jpg_quality"]
        interval = 1.0 / max_fps if max_fps > 0 else 0.0
        reader = FrameReader(streamCfg, max(interval, 0.01))
        try:
            last_seq = 0
            next_at = time.perf_counter()
            while True:
                seq, frame = reader.read()
                if seq == last_seq:
                    if reader.failed:
                        break
                    await asyncio.sleep(0.005)
                    continue
                last_seq = seq
                annotated = detect.detect(frame)
                ret, buffer = cv2.imencode(
                    ".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, jpg_quality]
                )
                if not ret:
                    logger.warn("编码失败，跳过本帧")
                    continue
                self._publish(buffer.tobytes())
                ready.set()
                next_at += interval
                remaining = next_at - time.perf_counter()
                if remaining <= 0:
                    next_at = time.perf_counter()
                    remaining = 0.0
                await asyncio.sleep(remaining)
        finally:
            reader.close()
            self._publish(None)
            ready.set()


hub = StreamHub()
