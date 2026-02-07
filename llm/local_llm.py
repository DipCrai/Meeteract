from os import cpu_count
from ui.main_window import MainWindow

def load_local_llm(model_path: str, window: MainWindow):
    from llama_cpp import Llama

    window.log("Загружаем локальную LLM...")

    llm = Llama(
        model_path=model_path,
        n_ctx=0,
        n_threads=max(1, (cpu_count() or 4) - 1),
        verbose=False,
        n_gpu_layers=1
    )

    return llm