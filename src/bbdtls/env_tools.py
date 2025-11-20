import os
from typing import Optional
from dotenv import load_dotenv

"""
Environment variable tools
"""

# 加载环境变量
def load_env(dotenv_path: Optional[str] = None):
    load_dotenv(dotenv_path or ".env")

# 获取环境变量
def get_env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

# 设置环境变量
def set_env(key: str, value: str):
    os.environ[key] = value
