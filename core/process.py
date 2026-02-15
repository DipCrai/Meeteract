from subprocess import run, DEVNULL

def run_hidden(cmd: list[str]):
    return run(
        cmd,
        check=True,
        stdout=DEVNULL,
        stderr=DEVNULL,
        stdin=DEVNULL
    )