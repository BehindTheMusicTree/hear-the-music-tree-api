import os
import shutil
import tempfile
import uuid
from pathlib import Path

from django.core.cache import cache

from api import settings

SESSION_TTL_SECONDS = 900  # 15 minutes
CACHE_KEY_PREFIX = "metadata_session:"


def _get_session_dir() -> Path:
    session_dir = getattr(settings, "METADATA_SESSION_DIR", None)
    if session_dir is not None:
        return session_dir
    return (Path(tempfile.gettempdir()) / "htmt_metadata_sessions").resolve()


def _ensure_session_dir() -> Path:
    d = _get_session_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


def create_session(source_file_path: str, original_filename: str) -> tuple[str, int]:
    """Store file in session dir, cache path and filename with TTL. Returns (token, ttl_seconds)."""
    ext = os.path.splitext(original_filename)[1] or ".bin"
    token = uuid.uuid4().hex
    session_dir = _ensure_session_dir()
    dest_path = session_dir / f"{token}{ext}"
    shutil.copy2(source_file_path, dest_path)
    cache_key = f"{CACHE_KEY_PREFIX}{token}"
    cache.set(
        cache_key,
        {"path": str(dest_path), "filename": original_filename},
        timeout=SESSION_TTL_SECONDS,
    )
    return token, SESSION_TTL_SECONDS


def get_session(token: str) -> tuple[str, str] | None:
    """Return (file_path, original_filename) if session exists and is not expired, else None."""
    if not token or not token.strip():
        return None
    cache_key = f"{CACHE_KEY_PREFIX}{token.strip()}"
    data = cache.get(cache_key)
    if not data or "path" not in data or "filename" not in data:
        return None
    path = data["path"]
    if not os.path.exists(path):
        return None
    return path, data["filename"]
