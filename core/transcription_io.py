def load_transcript(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_transcript(transcript: str) -> None:
    with open("transcript.txt", "w", encoding="utf-8") as f:
        for speaker, text in transcript:
            f.write(f"{speaker}: {text}\n")