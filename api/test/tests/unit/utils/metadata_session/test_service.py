import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.core.cache import cache

from api.utils.metadata_session import (
    SESSION_TTL_SECONDS,
    create_session,
    get_session,
)


class TestMetadataSessionService:
    def setup_method(self):
        cache.clear()

    def test_create_session_then_get_session_returns_path_and_filename(self):
        tmpdir = tempfile.mkdtemp()
        try:
            with patch("api.utils.metadata_session.service._get_session_dir") as m_dir:
                m_dir.return_value = Path(tmpdir)
                fd, path = tempfile.mkstemp(suffix=".mp3", dir=tmpdir)
                os.close(fd)
                token, ttl = create_session(path, "original.mp3")
                assert token
                assert len(token) == 32
                assert ttl == SESSION_TTL_SECONDS
                session = get_session(token)
                assert session is not None
                stored_path, filename = session
                assert os.path.exists(stored_path)
                assert filename == "original.mp3"
        finally:
            for f in Path(tmpdir).iterdir():
                try:
                    f.unlink()
                except OSError:
                    pass
            try:
                os.rmdir(tmpdir)
            except OSError:
                pass

    def test_get_session_invalid_token_then_none(self):
        assert get_session("") is None
        assert get_session("nonexistenttoken123") is None

    def test_get_session_after_cache_clear_then_none(self):
        tmpdir = tempfile.mkdtemp()
        try:
            with patch("api.utils.metadata_session.service._get_session_dir") as m_dir:
                m_dir.return_value = Path(tmpdir)
                fd, path = tempfile.mkstemp(suffix=".mp3", dir=tmpdir)
                os.close(fd)
                token, _ = create_session(path, "a.mp3")
                cache.clear()
                assert get_session(token) is None
        finally:
            for f in Path(tmpdir).iterdir():
                try:
                    f.unlink()
                except OSError:
                    pass
            try:
                os.rmdir(tmpdir)
            except OSError:
                pass
