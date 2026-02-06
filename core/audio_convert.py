from ui.logger import log
from core.paths import get_ffmpeg_path
from core.process import run_hidden
from os import path
from subprocess import CalledProcessError

def convert_to_wav(input_path: str, ui_text_widget, output_path: str = "temp_audio.wav") -> str | None:
    if not path.exists(input_path):
        log(ui_text_widget, "Файл не найден")
        return None

    if input_path.lower().endswith(".wav"):
        return input_path

    cmd = [
        get_ffmpeg_path(),
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]

    try:
        run_hidden(cmd)
        log(ui_text_widget, f"Конвертировано в WAV: {output_path}")
        return output_path
    except CalledProcessError:
        log(ui_text_widget, "Ошибка конвертации")
        return None