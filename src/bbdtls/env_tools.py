import os
from typing import Optional, TypeVar, cast
from dotenv import load_dotenv


T = TypeVar("T")

# Environment variable uration
class Env:
    def __init__(self, dotenv_path: Optional[str] = None):
        load_dotenv(dotenv_path or ".env")

    def get(self, key: str, default: T = None) -> T:
        return cast(T, os.getenv(key, default))

    def get_str(self, key: str, default: str = "") -> str:
        return os.getenv(key, default)

    def get_int(self, key: str, default: int = 0) -> int:
        val = os.getenv(key)
        return int(val) if val and val.isdigit() else default

    def get_bool(self, key: str, default: bool = False) -> bool:
        val = os.getenv(key, "").lower()
        return val in ("true", "1", "yes", "on") if val else default