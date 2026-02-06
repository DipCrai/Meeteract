from ui.logger import log

def transcribe_segments(wav_path: str, segments, ui_text_widget, model_name: str = "large"):
    from numpy import isfinite, nan_to_num
    from whisper import load_model
    from soundfile import read
    from torch.cuda import is_available

    log(ui_text_widget, "Запуск Whisper для транскрипции...")
    device = "cuda" if is_available() else "cpu"
    model = load_model(model_name, device=device)

    audio, sr = read(wav_path, dtype="float32")

    valid_segments = [seg for seg in segments if (seg["end"] - seg["start"]) >= 0.3]
    results = []
    pad = 0.15

    for i, seg in enumerate(valid_segments, start=1):
        start = max(0.0, float(seg["start"]) - pad)
        end = min(float(seg["end"]) + pad, len(audio) / sr)
        speaker = seg["speaker"]

        i0 = int(start * sr)
        i1 = int(end * sr)
        if i1 <= i0:
            continue

        segment_audio = audio[i0:i1]
        if not isfinite(segment_audio).all():
            segment_audio = nan_to_num(segment_audio)

        log(ui_text_widget, f"Транскрибируем сегмент {i}/{len(valid_segments)}...")

        try:
            res = model.transcribe(
                segment_audio,
                language="ru",
                fp16=is_available(),
                verbose=False,
                condition_on_previous_text=False
            )
            text = (res.get("text") or "").strip()
            if text:
                results.append((speaker, text))
        except Exception as e:
            log(ui_text_widget, f"Ошибка на сегменте {i}: {e}")

    log(ui_text_widget, "Транскрипция завершена")
    return results