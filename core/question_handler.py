from llm.chat import ask_gpt
from threading import Thread
import app

def ask_question():
    window = app.window
    llm = app.llm
    messages = app.messages

    user_input = window.get_user_input()

    if not user_input:
        return

    (window.clear_question_entry()
     .disable_questions()
     .log(f"\nВопрос: {user_input}")
     .log("Обрабатываю вопрос..."))

    def worker():
        try:
            answer = ask_gpt(llm, messages, user_input)
        except Exception as e:
            answer = f"Ошибка запроса: {e}"

        def finish():
            (window.log(f"Ответ: {answer}")
             .enable_questions())

        window.run_on_ui_thread(finish)

    Thread(target=worker, daemon=True).start()