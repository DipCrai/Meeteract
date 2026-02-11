from ui.main_window import MainWindow

def diarize_audio(file_path: str, window: MainWindow):
    window.log("Загружаем аудио для диаризации...")

    from torch import device
    from torchaudio import load
    from torch.cuda import is_available
    from pyannote.audio import Pipeline

    waveform, sample_rate = load(file_path)

    window.log("Загружаем модель диаризации...")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1")
    if is_available():
        pipeline.to(device("cuda"))

    window.log("Обрабатываем аудио...")
    output = pipeline({"waveform": waveform, "sample_rate": sample_rate})

    segments = []
    for turn, speaker in output.speaker_diarization:
            segments.append({"start": float(turn.start), "end": float(turn.end), "speaker": speaker})
    return segments