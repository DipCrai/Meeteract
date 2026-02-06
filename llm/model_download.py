from huggingface_hub import hf_hub_download

def download_qwen():
    return hf_hub_download(
        repo_id="paultimothymooney/Qwen2.5-7B-Instruct-Q4_K_M-GGUF",
        filename="qwen2.5-7b-instruct-q4_k_m.gguf"
    )