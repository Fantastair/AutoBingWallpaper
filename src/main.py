"""主文件"""

import sys
import os
import subprocess
import platform
import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING or sys.platform == "win32":
    import ctypes

import time

import requests

BASE_URL = "https://cn.bing.com"
API_URL = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=zh-CN&setlang=en"

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

IMG_TEMP_PATH = BASE_DIR / "temp_wallpaper.jpg"
LOG_FILE_PATH = BASE_DIR / "wallpaper_log.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def download_wallpaper() -> bytes | None:
    """下载今日壁纸"""
    logger.info("正在获取壁纸信息...")

    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    images = data.get("images", [])
    if not images:
        logger.warning("API 返回的图片列表为空")
        return None
    img_info = images[0]
    img_url = img_info.get("url")
    if not img_url:
        logger.warning("未获取到图片 URL")
        return None
    if img_url.startswith("/"):
        img_url = BASE_URL + img_url

    logger.info(f"正在下载壁纸: {img_url}")
    try:
        img_resp = requests.get(img_url, timeout=30)
        img_resp.raise_for_status()
        logger.info("壁纸下载成功")
        return img_resp.content
    except Exception as e:
        logger.error(f"壁纸下载失败: {e}")
        return None


def set_wallpaper_linux(file_path: str):
    """在 Linux 下设置壁纸，自动检测桌面环境"""
    uri = f"file://{file_path}"

    # 检测桌面环境
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    # 也检查 GDMSESSION 作为备选
    if not desktop:
        desktop = os.environ.get("GDMSESSION", "").lower()

    # GNOME / Unity / Budgie
    if any(d in desktop for d in ("gnome", "unity", "budgie")):
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri",
                uri,
            ],
            check=False,
        )
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                "picture-uri-dark",
                uri,
            ],
            check=False,
        )

    # KDE Plasma
    elif "kde" in desktop or "plasma" in desktop:
        subprocess.run(
            [
                "dbus-send",
                "--session",
                "--dest=org.kde.plasmashell",
                "--type=method_call",
                "/PlasmaShell",
                "org.kde.PlasmaShell.evaluateScript",
                f'string:var allDesktops = desktops();for (i=0;i<allDesktops.length;i++) {{d = allDesktops[i];d.wallpaperPlugin = "org.kde.image";d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");d.writeConfig("Image", "file://{file_path}")}}',
            ],
            check=False,
        )

    # XFCE
    elif "xfce" in desktop:
        subprocess.run(
            [
                "xfconf-query",
                "-c",
                "xfce4-desktop",
                "-p",
                "/backdrop/screen0/monitor0/workspace0/last-image",
                "-s",
                file_path,
            ],
            check=False,
        )

    # Cinnamon
    elif "cinnamon" in desktop:
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.cinnamon.desktop.background",
                "picture-uri",
                uri,
            ],
            check=False,
        )

    # MATE
    elif "mate" in desktop:
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.mate.background",
                "picture-filename",
                file_path,
            ],
            check=False,
        )

    # fallback: 尝试 feh（通用 X11 壁纸工具）
    else:
        subprocess.run(
            ["feh", "--bg-fill", file_path],
            check=False,
        )


def set_wallpaper_windows(file_path: str):
    """在 Windows 下设置壁纸"""
    windll = getattr(ctypes, "windll")
    windll.user32.SystemParametersInfoW(0x0014, 0, file_path, 3)


def set_wallpaper(wallpaper_bytes: bytes):
    """设置壁纸（跨平台）"""
    with IMG_TEMP_PATH.open("wb") as f:
        f.write(wallpaper_bytes)
    tmp_file_path = str(IMG_TEMP_PATH.resolve())

    system = platform.system()
    logger.info(f"正在设置 {system} 壁纸...")
    if system == "Windows":
        set_wallpaper_windows(tmp_file_path)
    elif system == "Linux":
        set_wallpaper_linux(tmp_file_path)
    else:
        raise OSError(f"不支持的操作系统: {system}")
    logger.info("壁纸设置完成")


if __name__ == "__main__":
    MAX_RETRIES = 5
    RETRY_DELAY = 5  # 秒

    logger.info("AutoBingWallpaper 启动")

    wallpaper_bytes = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            wallpaper_bytes = download_wallpaper()
            if wallpaper_bytes is not None:
                break
        except Exception as e:
            logger.error(f"第 {attempt} 次下载异常: {e}")

        if attempt < MAX_RETRIES:
            logger.info(f"第 {attempt} 次失败，{RETRY_DELAY} 秒后重试...")
            time.sleep(RETRY_DELAY)

    if wallpaper_bytes is not None:
        set_wallpaper(wallpaper_bytes)
    else:
        logger.error(f"下载壁纸失败，已重试 {MAX_RETRIES} 次")
