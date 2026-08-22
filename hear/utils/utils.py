import os
import random
import string


def print_django(message):
    print(f"[Django] {message}", flush=True)


def is_django_startup_verbose() -> bool:
    """When true, settings startup logs full OAuth client ids, redirect URIs, etc. Default: off (safer for container
    logs).
    """
    return os.environ.get("DJANGO_VERBOSE_STARTUP", "").strip().lower() in ("1", "true", "yes")


def mask_oauth_client_id(value: str, keep: int = 4) -> str:
    """Shorten OAuth *public* client ids for logs (not as sensitive as secrets; still avoid full value in stdout)."""
    v = (value or "").strip()
    if len(v) <= 2 * keep:
        return "***"
    return f"{v[:keep]}…{v[-keep:]}"


def generate_short_uu(length: int):
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_substring_after_last_slash(string: str):
    return string.rsplit("/", maxsplit=1)[-1]


def get_file_extension_from_url(url: str):
    return url.rsplit(".", maxsplit=1)[-1]


def print_file_status(file):
    file_name = getattr(file, "name", "Unknown file")

    if hasattr(file, "closed"):
        status = "CLOSED" if file.closed else "OPEN"
        print(f"File '{file_name}' is {status}")
        if not file.closed:
            print(f"Current position: {file.tell()}")
    else:
        print(f"File '{file_name}' status cannot be determined")
