"""Simple reachability check used by the admin ops console."
import subprocess
import shlex


def ping_host(host: str) -> str:
    """Ping a hostname / IP and return the stdout."""
    # Validate that host contains only safe characters
    if not host or not all(c.isalnum() or c in '.-:' for c in host):
        raise ValueError("Invalid host format")
    
    proc = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return proc.stdout