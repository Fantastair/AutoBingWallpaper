"""主文件"""

import os
import ctypes
import tempfile

import requests

BASE_URL = "https://cn.bing.com"
API_URL = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=zh-CN&setlang=en"


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
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
        tmp_file.write(wallpaper_bytes)
        tmp_file.flush()
        tmp_file_path = tmp_file.name

    ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, tmp_file_path, 3)

    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)


if __name__ == "__main__":
    wallpaper_bytes = download_wallpaper()
    if wallpaper_bytes is not None:
        set_wallpaper(wallpaper_bytes)
