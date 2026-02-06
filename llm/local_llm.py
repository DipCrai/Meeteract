from ui.logger import log
from os import cpu_count

def load_local_llm(model_path: str, ui_text_widget=None):
    from llama_cpp import Llama

    if ui_text_widget:
        log(ui_text_widget, "Загружаем локальную LLM...")

    llm = Llama(
        model_path=model_path,
        n_ctx=0,
        n_threads=max(1, (cpu_count() or 4) - 1),
        verbose=False,
        n_gpu_layers=1
    )
    return llm