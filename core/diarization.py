from ui.logger import log

def diarize_audio(file_path: str, ui_text_widget):
    log(ui_text_widget, "Загрузка аудио для диаризации...")

    from torch import device
    from torchaudio import load
    from torch.cuda import is_available
    from pyannote.audio import Pipeline

    waveform, sample_rate = load(file_path)

    log(ui_text_widget, "Загрузка модели диаризации...")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1")
    if is_available():
        pipeline.to(device("cuda"))

    log(ui_text_widget, "Обработка аудио...")
    output = pipeline({"waveform": waveform, "sample_rate": sample_rate})

    segments = []
    for turn, speaker in output.speaker_diarization:
            segments.append({"start": float(turn.start), "end": float(turn.end), "speaker": speaker})
    return segments