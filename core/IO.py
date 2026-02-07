from os import path, remove

def load_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_file(transcript: str, file_path: str = "transcript.txt") -> str:
    with open(file_path, "w", encoding="utf-8") as f:
        for speaker, text in transcript:
            f.write(f"{speaker}: {text}\n")
    return file_path

def remove_file(file_path: str = "transcript.txt") -> None:
    if path.exists(file_path):
        remove(file_path)