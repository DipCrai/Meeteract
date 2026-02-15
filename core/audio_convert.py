from core.paths import get_ffmpeg_path
from core.process import run_hidden

def convert_to_wav(input_path: str, output_path: str = "temp_audio.wav") -> str | None:
    for ffmpeg_bin in [get_ffmpeg_path(), "ffmpeg"]:
        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", input_path,
            "-ac", "1",
            "-ar", "16000",
            output_path
        ]
        try:
            run_hidden(cmd)
            return output_path
        except Exception:
            continue

    return None
