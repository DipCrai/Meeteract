from threading import Thread
from typing import Any

from core.audio_convert import convert_to_wav as core_convert_to_wav
from core.diarization import diarize_audio as core_diarize_audio
from core.transcription import transcribe_segments as core_transcribe_segments

from core.question_handler import ask_question
from core.IO import save_file, load_file

from llm.chat import init_gpt, summarize_meeting
from ui.main_window import MainWindow

def summarize(window: MainWindow):
    analysis = Analysis(window)

    window.disable_controls()

    try:
        llm, messages = analysis.init_gpt()
        analysis.summarize(llm, messages)
        window.set_question_handler(lambda: ask_question(window, llm, messages)).enable_questions()
    except Exception as e:
        window.log(f"Ошибка резюме: {e}").enable_controls().disable_questions()

class Analysis:
    def __init__(self, window: MainWindow):
        self.window = window

    def choose_file(self) -> str | None:
        file_path = self.window.get_selected_file_path()

        if not file_path:
            self.window.log("Файл не выбран")
            return None

        return file_path

    def convert_to_wav(self) -> str | None:
        file_path = self.choose_file()

        if file_path is None:
            return None

        self.window.log(f"Конвертируем в WAV: {file_path}...")
        return core_convert_to_wav(file_path)

    def diarize_audio(self) -> Any | None:
        file_path = self.convert_to_wav()

        if file_path is None:
            return None

        self.window.log("Начинаем диаризацию...")
        return file_path, core_diarize_audio(file_path, self.window)

    def transcribe_segments(self) -> Any | None:
        wav_path, segments = self.diarize_audio()

        if wav_path is None or segments is None:
            return None

        self.window.log("Транскрибируем сегменты...")
        return core_transcribe_segments(wav_path, segments, self.window)

    def save_transcript(self) -> str | None:
        transcription = self.transcribe_segments()

        if transcription is None:
            return None

        self.window.log("Сохраняем транскрипт...")
        return save_file(transcription)

    def load_transcript(self) -> str | None:
        file_path = self.save_transcript()

        if file_path is None:
            return None

        self.window.log("Загружаем транскрипт...")
        return load_file(file_path)

    def init_gpt(self) -> Any | None:
        transcript_text: str = self.load_transcript()

        if transcript_text is None:
            return None

        self.window.log("Инициализируем локальную LLM...")
        return init_gpt(transcript_text, self.window)

    def summarize(self, llm, messages):
        self.window.log("\nРЕЗЮМЕ ВСТРЕЧИ:\n")

        summary = summarize_meeting(llm, messages)
        self.window.log(summary)

def start_summarize_thread(window: MainWindow):
    Thread(target= lambda: summarize(window), daemon=True).start()