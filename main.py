from core.analysis import start_summarize_thread
from ui.main_window import MainWindow
import app

if __name__ == "__main__":
    app.window = window = MainWindow()
    window.set_start_handler(start_summarize_thread)
    window.run()