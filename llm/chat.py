from llm.local_llm import load_local_llm
from llm.model_download import download_qwen
from ui.main_window import MainWindow

def qwen_format_messages(messages) -> str:
    parts = []
    for m in messages:
        role = m["role"]
        content = m["content"]
        parts.append(f"<|im_start|>{role}\n{content}\n<|im_end|>")
    parts.append("<|im_start|>assistant\n")
    return "\n".join(parts)

def local_llm_chat(llm, messages, temperature=0.2, max_tokens=256) -> str:
    prompt = qwen_format_messages(messages)
    out = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.95,
        stop=["<|im_end|>", "<|im_start|>"]
    )
    return (out["choices"][0]["text"] or "").strip()

def init_gpt(transcript_text: str, window: MainWindow):
    system_prompt = f"""
    Ты аналитик онлайн-конференций.

    У тебя есть транскрипт встречи.
    Ты должен:
    - отвечать ТОЛЬКО на основе транскрипта
    - если информации в транскрипте нет — не выдумывать факты
    - давать развернутый ответ, но не слишком, если только пользователь не попросит краткости
    - если транскрипт не похож на онлайн-конференцию, (пользователь мог загрузить не ту запись) уведомить пользователя об этом
    - давать ответы чистым текстом, БЕЗ РАЗМЕТОК по-типу markdown

    ТРАНСКРИПТ:
    {transcript_text}
    """.strip()

    model_path = download_qwen()
    llm = load_local_llm(model_path, window)

    state = {
        "system": {"role": "system", "content": system_prompt},
        "memory": [],
    }
    return llm, state

def _build_messages(state, user_input: str, memory_turns: int = 2):
    if memory_turns <= 0:
        mem = []
    else:
        mem = state["memory"][-2 * memory_turns:]
    return [state["system"], *mem, {"role": "user", "content": user_input}]

def ask_gpt(llm, state, user_input: str):
    messages = _build_messages(state, user_input, memory_turns=2)
    answer = local_llm_chat(llm, messages, temperature=0.2)

    state["memory"].append({"role": "user", "content": user_input})
    state["memory"].append({"role": "assistant", "content": answer})

    if len(state["memory"]) > 20:
        state["memory"] = state["memory"][-20:]

    return answer

def summarize_meeting(llm, state):
    summary_prompt = """
    Сделай краткое резюме встречи:
    - основные темы
    - ключевые решения
    - выводы, сделанные на конференции
    """.strip()

    messages = _build_messages(state, summary_prompt, memory_turns=0)
    summary = local_llm_chat(llm, messages, temperature=0.2)

    state["memory"].append({"role": "user", "content": summary_prompt})
    state["memory"].append({"role": "assistant", "content": summary})
    if len(state["memory"]) > 20:
        state["memory"] = state["memory"][-20:]

    return summary