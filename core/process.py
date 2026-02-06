from subprocess import run, DEVNULL, CREATE_NO_WINDOW

def run_hidden(cmd: list[str]):
    return run(
        cmd,
        check=True,
        stdout=DEVNULL,
        stderr=DEVNULL,
        stdin=DEVNULL,
        creationflags=CREATE_NO_WINDOW
    )