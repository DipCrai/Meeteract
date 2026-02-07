from huggingface_hub import login

from config import HF_TOKEN
from core.analysis import start_summarize_thread
from ui.main_window import MainWindow

import app

if __name__ == "__main__":
    login(HF_TOKEN)
    app.window = window = MainWindow()
    window.set_start_handler(start_summarize_thread)
    window.run()