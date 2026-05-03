"""
从pyproject.toml获取项目的版本号。
任何地方都应该使用这个脚本获取版本号，确保版本号的一致性以及可维护性。
"""

import tomllib
from pathlib import Path

__all__ = ["get_version", "PYPROJECT_PATH"]

CWD = Path(__file__).parent
PYPROJECT_PATH = CWD.parent / "pyproject.toml"


def get_version() -> str:
    """从pyproject.toml获取项目的版本号"""
    with PYPROJECT_PATH.open("rb") as f:
        pyproject_data = tomllib.load(f)
    return pyproject_data["project"]["version"]


if __name__ == "__main__":
    print(get_version())
