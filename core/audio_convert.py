from core.paths import get_ffmpeg_path
from core.process import run_hidden
from subprocess import CalledProcessError

def convert_to_wav(input_path: str, output_path: str = "temp_audio.wav") -> str | None:
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
        return output_path
    except CalledProcessError:
        return None