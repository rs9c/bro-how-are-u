from pathlib import Path
from typing import cast

import numpy as np
import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results

from app.services import config, logger

if torch.cuda.is_available():
    _DEVICE = "cuda"
elif torch.backends.mps.is_available():
    _DEVICE = "mps"
else:
    _DEVICE = "cpu"

_MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
_modelCfg: dict = config.cfg["model"]

_model = YOLO(_MODELS_DIR / _modelCfg["path"])
_model.to(_DEVICE)

logger.info(f"模型路径：{_MODELS_DIR / _modelCfg['path']}  设备：{_DEVICE}")

_model.predict(
    source=np.zeros((640, 640, 3), dtype=np.uint8), device=_DEVICE, verbose=False
)

logger.info("模型预热完成")


def detect(frame):
    """
    检测单帧并返回标注结果
    """
    results = cast(
        list[Results],
        _model.predict(source=frame, device=_DEVICE, verbose=False, stream=False),
    )
    annotated = results[0].plot()
    return annotated
