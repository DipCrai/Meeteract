from huggingface_hub import login

from config import HF_TOKEN
from core.analysis import start_summarize_thread
from ui.main_window import MainWindow

if __name__ == "__main__":
    login(HF_TOKEN)
    window = MainWindow()
    (window.set_start_handler(lambda: start_summarize_thread(window))
     .run())