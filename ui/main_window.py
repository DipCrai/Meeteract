from tkinter import (
    filedialog, Frame, Entry, Tk,
    Button, Text, END, StringVar
)
from os import path

class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("ИИ Помощник для онлайн конференций (Qwen2.5-7B)")
        self.root.geometry("700x520")
        self.root.resizable(False, False)

        self.log_text = Text(self.root, wrap="word", state="disabled", height=20)
        self.log_text.pack(fill="x", padx=10, pady=(10, 6))

        self.selected_file = StringVar()

        controls = Frame(self.root)
        controls.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_choose_file = Button(controls, text="Выбрать файл", command=self.choose_file)
        self.btn_choose_file.pack(fill="x", pady=(0, 6))

        self.btn_start = Button(controls, text="Начать анализ")
        self.btn_start.pack(fill="x", pady=(0, 10))

        self.entry_question = Entry(controls)
        self.entry_question.pack(fill="x", pady=(0, 6))

        self.btn_ask = Button(controls, text="Задать вопрос")
        self.btn_ask.pack(fill="x")

        self.disable_questions()

    def choose_file(self) -> "MainWindow":
        file_path = filedialog.askopenfilename(
            title="Выберите аудио или видео файл"
        )
        if file_path:
            self.selected_file.set(file_path)
            self.btn_choose_file.config(text=path.basename(file_path))
        return self

    def log(self, message: str) -> "MainWindow":
        def append_text():
            self.log_text.configure(state="normal")
            self.log_text.insert(END, message + "\n")
            self.log_text.see(END)
            self.log_text.configure(state="disabled")

        try:
            self.log_text.after(0, append_text)
        except Exception:
            pass

        return self

    def enable_questions(self) -> "MainWindow":
        self.btn_ask.config(state="normal")
        self.entry_question.config(state="normal")
        return self

    def disable_questions(self) -> "MainWindow":
        self.btn_ask.config(state="disabled")
        self.entry_question.config(state="disabled")
        return self

    def set_start_handler(self, start_handler) -> "MainWindow":
        self.btn_start.config(command=start_handler)
        return self

    def set_question_handler(self, question_handler) -> "MainWindow":
        self.btn_ask.config(command=question_handler)
        return self

    def disable_controls(self):
        self.btn_choose_file.config(state="disabled")
        self.btn_ask.config(state="disabled")
        self.btn_start.config(state="disabled")
        self.entry_question.config(state="disabled")
        return self

    def enable_controls(self):
        self.btn_choose_file.config(state="normal")
        self.btn_ask.config(state="normal")
        self.btn_start.config(state="normal")
        self.entry_question.config(state="normal")
        return self

    def clear_question_entry(self) -> "MainWindow":
        self.entry_question.delete(0, END)
        return self

    def get_user_input(self) -> str:
        return self.entry_question.get().strip()

    def get_selected_file_path(self) -> str:
        return self.selected_file.get().strip()

    def run_on_ui_thread(self, func) -> None:
        self.root.after(0, func)

    def run(self) -> "MainWindow":
        self.root.mainloop()
        return self