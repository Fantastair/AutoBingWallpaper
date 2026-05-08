"""主文件"""

import sys
import ctypes
from pathlib import Path

import requests

BASE_URL = "https://cn.bing.com"
API_URL = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=zh-CN&setlang=en"

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

IMG_TEMP_PATH = BASE_DIR / "temp_wallpaper.jpg"


def download_wallpaper() -> bytes | None:
    """下载今日壁纸"""

    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    images = data.get("images", [])
    if not images:
        return
    img_info = images[0]
    img_url = img_info.get("url")
    if not img_url:
        return
    if img_url.startswith("/"):
        img_url = BASE_URL + img_url

    try:
        img_resp = requests.get(img_url, timeout=30)
        img_resp.raise_for_status()
        return img_resp.content
    except Exception:
        return


def set_wallpaper(wallpaper_bytes: bytes):
    """设置壁纸"""
    with IMG_TEMP_PATH.open("wb") as f:
        f.write(wallpaper_bytes)
    tmp_file_path = str(IMG_TEMP_PATH.resolve())

    ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, tmp_file_path, 3)


if __name__ == "__main__":
    wallpaper_bytes = download_wallpaper()
    if wallpaper_bytes is not None:
        set_wallpaper(wallpaper_bytes)
