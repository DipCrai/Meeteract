from os import path, makedirs
import sys

def get_base_dir() -> str:
    if getattr(sys, "frozen", False):
        return path.dirname(sys.executable)
    return path.dirname(path.abspath(__file__))


def get_ffmpeg_path():
    ffmpeg_path = path.join(get_base_dir(), "ffmpeg.exe")
    if not path.exists(ffmpeg_path):
        raise FileNotFoundError(f"ffmpeg.exe не найден: {ffmpeg_path}")
    return ffmpeg_path

def get_app_cache_dir() -> str:
    base = path.join(path.expanduser("~"), ".cache")
    makedirs(base, exist_ok=True)
    return base