import json
import shutil
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _APP_DIR / "config.json"
_TEMPLATE_PATH = _APP_DIR / "config-template.json"


def _load() -> dict:
    if not _CONFIG_PATH.exists():
        shutil.copyfile(_TEMPLATE_PATH, _CONFIG_PATH)
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


cfg = _load()

# TODO 目前手动修改config.json后需要重启才能生效


def save(cfg: dict) -> None:
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=4)
