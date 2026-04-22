"""Simple reachability check used by the admin ops console."
import subprocess
import shlex


def ping_host(host: str) -> str:
    """Ping a hostname / IP and return the stdout."""
    # Validate input to prevent command injection
    if not host or any(char in host for char in [';', '&', '|', '`', '$', '(', ')', '<', '>', '\n', '\r']):
        raise ValueError("Invalid host parameter")
    
    proc = subprocess.run(
        ["ping", "-c", "1", host],
        shell=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return proc.stdout