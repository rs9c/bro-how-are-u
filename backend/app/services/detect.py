from pathlib import Path
from typing import cast

import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results

from app.services import config, logger

_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

_MODELS_DIR = Path(__file__).resolve().parent.parent.parent / "models"
_modelCfg: dict = config.cfg["model"]

_model = YOLO(_MODELS_DIR / _modelCfg["path"])
_model.to(_DEVICE)

logger.info(f"模型路径：{_MODELS_DIR / _modelCfg['path']}  设备：{_DEVICE}")


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
