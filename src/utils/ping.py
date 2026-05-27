"""Simple reachability check used by the admin ops console."""
import subprocess


def ping_host(host: str) -> str:
    """Ping a hostname / IP and return the stdout."""
    proc = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return proc.stdout