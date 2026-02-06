from ui.logger import log
from core.diarization import diarize_audio
from core.transcription import transcribe_segments
from core.audio_convert import convert_to_wav
from core.transcription_io import save_transcript, load_transcript
from llm.chat import init_gpt, summarize_meeting, ask_gpt
from os import path, remove
from threading import Thread
from tkinter import filedialog, DISABLED, WORD, Frame, Entry, Button, Tk, X, Text, END, NORMAL, StringVar
from huggingface_hub import login
from config import HF_TOKEN

def main():
    login(HF_TOKEN)
    root = Tk()
    root.title("ИИ Помощник для онлайн конференций (Qwen2.5-7B)")
    root.geometry("700x520")
    root.resizable(False, False)

    log_text = Text(root, wrap=WORD, state=DISABLED, height=20)
    log_text.pack(fill=X, padx=10, pady=(10, 6))

    controls = Frame(root)
    controls.pack(fill=X, padx=10, pady=(0, 10))

    selected_file = StringVar()

    def choose_file():
        file_path = filedialog.askopenfilename(
            title="Выберите аудио или видео файл"
        )
        if file_path:
            selected_file.set(file_path)
            btn_choose_file.config(text=path.basename(file_path))

    btn_choose_file = Button(controls, text="Выбрать файл", command=choose_file)
    btn_choose_file.pack(fill=X, pady=(0, 6))

    btn_start = Button(controls, text="Начать анализ")
    btn_start.pack(fill=X, pady=(0, 10))

    entry_question = Entry(controls)
    entry_question.pack(fill=X, pady=(0, 6))

    btn_ask = Button(controls, text="Задать вопрос")
    btn_ask.pack(fill=X)
    btn_ask.config(state=DISABLED)

    def start_analysis_thread():
        Thread(target=start_analysis, daemon=True).start()

    btn_start.config(command=start_analysis_thread)

    def start_analysis():
        file_path = selected_file.get()

        if not file_path:
            log(log_text, "Файл не выбран")
            return

        root.after(0, lambda: btn_start.config(state=DISABLED))

        log(log_text, f"Конвертируем {file_path}...")
        wav_file = convert_to_wav(file_path, log_text)
        if not wav_file:
            log(log_text, "Ошибка конвертации")
            root.after(0, lambda: btn_start.config(state=NORMAL))
            return

        log(log_text, "Начинаем диаризацию...")
        segments = diarize_audio(wav_file, log_text)
        log(log_text, f"Сегментов найдено: {len(segments)}")

        log(log_text, "Транскрибируем сегменты...")
        transcript = transcribe_segments(wav_file, segments, log_text)

        save_transcript(transcript)

        log(log_text, "Транскрипт сохранен в transcript.txt")

        transcript_text = load_transcript("transcript.txt")

        log(log_text, "Инициализация локальной LLM...")
        llm, messages = init_gpt(transcript_text, log_text)

        log(log_text, "\nРЕЗЮМЕ ВСТРЕЧИ:\n")
        try:
            summary = summarize_meeting(llm, messages)
            log(log_text, summary)
        except Exception as e:
            log(log_text, f"Ошибка резюме: {e}")

        def ask_question():
            user_input = entry_question.get().strip()
            if not user_input:
                return

            entry_question.delete(0, END)
            btn_ask.config(state=DISABLED)
            entry_question.config(state=DISABLED)

            log(log_text, f"\nВопрос: {user_input}")
            log(log_text, "Обрабатываю вопрос...")

            def worker():
                try:
                    answer = ask_gpt(llm, messages, user_input)
                except Exception as e:
                    answer = f"Ошибка запроса: {e}"

                def finish():
                    log(log_text, f"Ответ: {answer}")
                    entry_question.config(state=NORMAL)
                    btn_ask.config(state=NORMAL)

                root.after(0, finish)

            Thread(target=worker, daemon=True).start()

        def enable_questions():
            btn_ask.config(command=ask_question, state=NORMAL)
            entry_question.config(state=NORMAL)
            btn_start.config(state=NORMAL)

        root.after(0, enable_questions)

        if wav_file != file_path and path.exists(wav_file):
            remove(wav_file)

    root.mainloop()


if __name__ == "__main__":
    main()
