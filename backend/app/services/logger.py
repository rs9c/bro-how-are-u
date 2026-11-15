from datetime import datetime

_COLORS = {
    "INFO": "\033[32m",   # 绿
    "WARN": "\033[33m",   # 黄
    "ERROR": "\033[31m",  # 红
}
_RESET = "\033[0m"


def _log(level: str, content: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = _COLORS.get(level, "")
    print(f"{color}[{now}] [{level}] {content}{_RESET}")


def info(content: str) -> None:
    _log("INFO", content)


def warn(content: str) -> None:
    _log("WARN", content)


def error(content: str) -> None:
    _log("ERROR", content)