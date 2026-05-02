import os
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from _pytest.main import Session
from django.test import override_settings

from api import settings

E2E_REACHABILITY_TIMEOUT_SEC = 5


@pytest.fixture(autouse=True)
def set_debug_for_tests():
    """Set DEBUG=True by default for tests.

    Individual tests can use @override_settings(DEBUG=False) when needed.
    """
    with override_settings(DEBUG=True):
        yield


def _is_ci() -> bool:
    return os.environ.get("ENV") == "ci_test"


def _should_mock_external_services(request) -> bool:
    """True when external services (OAuth, MusicBrainz, Spotify API) should be mocked: CI or non-e2e."""
    is_e2e = request.node.get_closest_marker("e2e") or "/tests/e2e/" in str(request.fspath)
    return _is_ci() or not is_e2e


# External service mocks below use empty/minimal responses. Tests that need non-empty data
# (e.g. a recording, token, search results) should patch the same target and set return values.


@pytest.fixture(autouse=True)
def mock_oauth_outside_e2e(request):
    """Mock Spotify and Google OAuth at the view layer.

    Env must have all optional services enabled; this fixture only applies boundary patches.
    Tests that need the disabled branch use @override_settings(SPOTIFY_ENABLED=False) or
    GOOGLE_OAUTH_ENABLED=False.
    """
    if not _should_mock_external_services(request):
        yield
        return
    with patch("api.view.spotify_auth.SpotifyOAuthService"), patch("api.view.google_auth.GoogleOAuthService"):
        yield


@pytest.fixture(autouse=True)
def mock_musicbrainz_outside_e2e(request):
    """Mock AcoustID/MusicBrainz lookup so no real API calls are made.

    Env must have MUSICBRAINZ_LOOKUP_ENABLED true; this fixture only applies the boundary patch
    (or none when the test uses @pytest.mark.patches_musicbrainz_lookup).
    Tests that need the disabled branch use @override_settings(MUSICBRAINZ_LOOKUP_ENABLED=False).
    """
    if not _should_mock_external_services(request):
        yield
        return
    if request.node.get_closest_marker("patches_musicbrainz_lookup"):
        yield
        return
    with patch(
        "api.utils.musicbrainz.service.acoustid.lookup",
        return_value={"status": "ok", "results": []},
    ):
        yield


def _make_spotify_client_mock():
    """Return a MagicMock configured as SpotifyClient with safe no-op responses."""
    m = MagicMock()
    m.search_track.return_value = {"tracks": {"items": []}}
    m.retrieve_track_by_id.return_value = {"id": ""}
    m.get_user_saved_tracks.return_value = {"items": []}
    m.get_user_playlists.return_value = {"items": []}
    m.get_playlist_tracks.return_value = {"items": []}
    m.get_track.return_value = {}
    m.get_user_profile.return_value = {}
    m.spotify.artists.return_value = {"artists": []}
    return m


@pytest.fixture(autouse=True)
def mock_spotify_client_outside_e2e(request):
    """Mock Spotify API client (library, search, playlists) so no real Spotify Web API calls are made.

    - When ENV=ci_test: always mock for all tests, including e2e.
    - In dev: mock only for non-e2e tests; e2e tests can use real Spotify API or their own mocks.
    """
    if _should_mock_external_services(request):
        mock_instance = _make_spotify_client_mock()
        with (
            patch(
                "api.utils.spotify_api.managers.SpotifyApiLibTrackManager.get_spotify_client",
                return_value=mock_instance,
            ),
            patch(
                "api.utils.spotify_api.managers.SpotifyApiArtistManager.get_spotify_client",
                return_value=mock_instance,
            ),
            patch(
                "api.view.viewset.model.SpotifyArtistViewSet.get_spotify_client",
                return_value=mock_instance,
            ),
        ):
            yield
    else:
        yield


def _is_e2e(request) -> bool:
    """True when the test is an e2e test (e2e marker or under tests/e2e/)."""
    return bool(request.node.get_closest_marker("e2e")) or "/tests/e2e/" in str(request.fspath)


def _make_success_fingerprinting_result():
    from api.model.uploaded_track.file.fingerprinting.FingerprintingResult import FingerprintingResult

    return FingerprintingResult(fingerprint=b"\x00" * 20, duration_in_sec=120, error=None)


@pytest.fixture(autouse=True)
def mock_audio_meta_analysis_outside_e2e(request):
    """Run audio meta analysis path with mocked AFP in non-e2e tests; e2e tests use real AFP.

    Env must have AFP_ENABLED true; this fixture only mocks get_fingerprinting_result for non-e2e.
    Tests that need real AFP use @pytest.mark.requires_real_afp to skip the mock.
    """
    is_e2e = _is_e2e(request)
    if is_e2e:
        yield
        return

    if request.node.get_closest_marker("requires_real_afp"):
        yield
        return

    with patch(
        "api.utils.audio_fingerprinter.service.get_fingerprinting_result",
        return_value=_make_success_fingerprinting_result(),
    ):
        yield


critical_test_failed = False


IGNORED_TEST_DIRS = [
    "utils/",
]


def pytest_ignore_collect(collection_path: Path, config):
    str_path = str(collection_path)
    return any(ignored_dir in str_path for ignored_dir in IGNORED_TEST_DIRS)


def base_childinstance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown


def _is_optional_service_enabled(attr_name: str) -> bool:
    """True if the flag is enabled on settings or in os.environ (e.g. from .env before setup_media_dirs runs)."""
    val = getattr(settings, attr_name, None)
    if val is None:
        val = os.environ.get(attr_name, "")
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


def _require_optional_services_enabled() -> None:
    """All optional services must be enabled to run tests; fail fast if any is disabled."""
    disabled: list[str] = []
    if not _is_optional_service_enabled("SPOTIFY_ENABLED"):
        disabled.append("SPOTIFY_ENABLED")
    if not _is_optional_service_enabled("GOOGLE_OAUTH_ENABLED"):
        disabled.append("GOOGLE_OAUTH_ENABLED")
    if not _is_optional_service_enabled("MUSICBRAINZ_LOOKUP_ENABLED"):
        disabled.append("MUSICBRAINZ_LOOKUP_ENABLED")
    if disabled:
        pytest.exit(
            f"All optional services must be enabled to run tests. Disabled: {', '.join(disabled)}. "
            f"Set them to true in env (CI: workflow env; dev: .env) and use fake credentials if not calling real APIs.",
            returncode=2,
        )


def _pytest_log(msg: str) -> None:
    """Visible progress during sessionstart/collection (avoids 'hangs' after Django settings load)."""
    print(f"[pytest] {msg}", flush=True)


def pytest_sessionstart(session: Session) -> None:
    _pytest_log("sessionstart: checking ffprobe (after Django settings; next is test collection)")
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None:
        pytest.exit(
            "ffprobe is required for tests (e.g. WAV duration) but was not found. "
            "Install ffmpeg (e.g. apt install ffmpeg or brew install ffmpeg).",
            returncode=2,
        )
    result = subprocess.run(
        [ffprobe, "-version"],
        capture_output=True,
        timeout=5,
        check=False,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or b"").decode("utf-8", errors="replace").strip()
        pytest.exit(
            "ffprobe is required for tests but failed to run (missing or broken dependencies, e.g. libvpx). "
            "On macOS with Homebrew, try: brew reinstall ffmpeg. "
            f"ffprobe output: {err or result.returncode}",
            returncode=2,
        )
    wav_fixture = Path(__file__).parent.parent / "utils" / "uploaded_track" / "files" / "duration=472s.wav"
    if wav_fixture.exists():
        _pytest_log(f"sessionstart: probing WAV fixture ({wav_fixture.name}, timeout 30s)")
        probe_result = subprocess.run(
            [ffprobe, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(wav_fixture)],
            capture_output=True,
            timeout=30,
            check=False,
        )
        if probe_result.returncode != 0:
            err = (probe_result.stderr or probe_result.stdout or b"").decode("utf-8", errors="replace").strip()
            pytest.exit(
                "ffprobe could not probe the WAV fixture (duration=472s.wav). Fix ffmpeg or the fixture. "
                f"ffprobe output: {err or probe_result.returncode}",
                returncode=2,
            )
    _pytest_log("sessionstart: ffprobe checks OK; collecting tests (this can take a while with no output)")


def pytest_configure(config):
    config.addinivalue_line("markers", "critical: mark test as critical to pass")
    config.addinivalue_line("markers", "slow: mark test as long-running")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end (may require network or external services)")
    config.addinivalue_line(
        "markers",
        "requires_real_afp: skip AFP mock so the test calls the real audio fingerprinting service",
    )
    config.addinivalue_line(
        "markers",
        "patches_musicbrainz_lookup: test patches acoustid.lookup itself; conftest only enables MB path",
    )


def _run_has_e2e_tests(session: Session) -> bool:
    for item in session.items:
        if item.get_closest_marker("e2e") or "/tests/e2e/" in str(item.fspath):
            return True
    return False


def _is_e2e_item(item) -> bool:
    return bool(item.get_closest_marker("e2e") or "/tests/e2e/" in str(item.fspath))


def _e2e_reachability_failures() -> list[str]:
    """Return list of unreachable service messages, or empty if all reachable."""
    failures: list[str] = []
    if getattr(settings, "SPOTIFY_ENABLED", False):
        ok, reason = _check_spotify_reachable()
        if not ok:
            failures.append(f"Spotify ({reason})")
    if getattr(settings, "GOOGLE_OAUTH_ENABLED", False):
        ok, reason = _check_google_reachable()
        if not ok:
            failures.append(f"Google OAuth ({reason})")
    if getattr(settings, "AFP_ENABLED", False):
        ok, reason = _check_afp_reachable()
        if not ok:
            failures.append(f"AFP ({reason})")
    if getattr(settings, "MUSICBRAINZ_LOOKUP_ENABLED", False):
        ok, reason = _check_musicbrainz_reachable()
        if not ok:
            failures.append(f"MusicBrainz (AcoustID) ({reason})")
    return failures


def _check_url_reachable(url: str) -> tuple[bool, str]:
    try:
        req = urllib.request.Request(url, method="HEAD")
        urllib.request.urlopen(req, timeout=E2E_REACHABILITY_TIMEOUT_SEC)
        return True, ""
    except urllib.error.HTTPError as e:
        if 400 <= e.code < 500:
            return True, ""
        return False, str(e) or type(e).__name__
    except Exception as e:
        try:
            urllib.request.urlopen(url, timeout=E2E_REACHABILITY_TIMEOUT_SEC)
            return True, ""
        except urllib.error.HTTPError as e2:
            if 400 <= e2.code < 500:
                return True, ""
            return False, str(e2) or type(e2).__name__
        except Exception as e2:
            return False, str(e2) or type(e2).__name__


def _check_afp_reachable() -> tuple[bool, str]:
    base = getattr(settings, "AFP_BASE_URL", None)
    port = getattr(settings, "AFP_PORT", None)
    if not base or not port:
        return False, "AFP_BASE_URL/AFP_PORT not set (AFP disabled or not configured)"
    health_url = f"http://{base}:{port}/health/"
    try:
        req = urllib.request.Request(health_url, method="GET")
        with urllib.request.urlopen(req, timeout=E2E_REACHABILITY_TIMEOUT_SEC) as resp:
            if 200 <= resp.status < 300:
                return True, ""
            return False, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, str(e) or type(e).__name__
    except Exception as e:
        return False, str(e) or type(e).__name__


def _check_spotify_reachable() -> tuple[bool, str]:
    return _check_url_reachable("https://accounts.spotify.com")


def _check_google_reachable() -> tuple[bool, str]:
    return _check_url_reachable("https://accounts.google.com")


def _check_musicbrainz_reachable() -> tuple[bool, str]:
    return _check_url_reachable("https://api.acoustid.org")


def pytest_collection_finish(session: Session) -> None:
    _pytest_log(f"collection_finish: {len(session.items)} items; checking optional services / e2e reachability")
    _require_optional_services_enabled()
    if not _run_has_e2e_tests(session):
        return
    if _is_ci():
        if not getattr(settings, "AFP_ENABLED", False):
            pytest.exit(
                "E2E tests require AFP. In CI (ENV=ci_test), AFP_ENABLED must be true.",
                returncode=2,
            )
        ok, reason = _check_afp_reachable()
        if not ok:
            pytest.exit(
                f"E2E tests require AFP. In CI (ENV=ci_test), the AFP service is unreachable. Reason: {reason}",
                returncode=2,
            )
        return
    failures = _e2e_reachability_failures()
    if failures:
        pytest.exit(
            "E2E run requires all enabled services to be reachable. Unreachable: " + "; ".join(failures),
            returncode=2,
        )


def pytest_runtest_makereport(item, call):
    global critical_test_failed
    critical_marker = item.get_closest_marker("critical")
    if call.when == "call" and critical_marker:
        if call.excinfo:
            critical_test_failed = True
            print(f"\nCRITICAL TEST FAILED: {item.name}")
            print(f"Output: {call.excinfo}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    if critical_test_failed:
        pytest.skip("A critical test has failed. Skipping the rest of the tests..")


def _get_test_directory_order(item) -> int:
    """Get the order priority for a test based on its directory structure.

    Returns:
        int: Order priority (lower = earlier execution)
        - 0: tests/critical/
        - 1: tests/unit/
        - 2: tests/integration/
        - 3: tests/e2e/
        - 4: other directories
    """
    test_path = str(item.fspath)
    if "/tests/critical/" in test_path:
        return 0
    if "/tests/unit/" in test_path:
        return 1
    if "/tests/integration/" in test_path:
        return 2
    if "/tests/e2e/" in test_path:
        return 3
    return 4


def pytest_collection_modifyitems(config, items):
    # Order tests: critical marker first, then by directory (critical → unit → integration → e2e), slow marker last
    critical_tests = []
    normal_tests = []
    slow_tests = []

    print(
        "Ordering tests: critical marker first, then by directory (tests/critical → tests/unit → tests/integration → tests/e2e), slow marker last"
    )
    for item in items:
        critical_marker = item.get_closest_marker("critical")
        slow_marker = item.get_closest_marker("slow")

        if critical_marker:
            critical_tests.append(item)
        elif slow_marker:
            slow_tests.append(item)
        else:
            normal_tests.append(item)

    # Sort each category by directory order
    critical_tests.sort(key=_get_test_directory_order)
    normal_tests.sort(key=_get_test_directory_order)
    slow_tests.sort(key=_get_test_directory_order)

    ordered = critical_tests + normal_tests + slow_tests
    is_ci = os.environ.get("ENV") == "ci_test"
    if not is_ci and any(_is_e2e_item(it) for it in ordered):
        failures = _e2e_reachability_failures()
        if failures:
            ordered = [it for it in ordered if not _is_e2e_item(it)]
            print("\nE2E tests deselected (services unreachable): " + "; ".join(failures) + "\n")
    items[:] = ordered


def _cleanup_test_user_directories() -> None:
    """Cleanup test user library directories.

    This function removes all test user library directories that start with
    TEST_USER_LIBRARIES_DIR_NAME_PREFIXE. It's called from multiple hooks to ensure
    cleanup happens even if tests are interrupted or fail.
    """
    libraries_path = Path(settings.LIBRARIES_DIR)
    removed_dirs: list[str] = []
    failed_dirs: list[str] = []

    try:
        if not libraries_path.exists():
            return

        for entry in libraries_path.iterdir():
            if entry.is_dir() and entry.name.startswith(settings.TEST_USER_LIBRARIES_DIR_NAME_PREFIXE):
                try:
                    shutil.rmtree(entry)
                    removed_dirs.append(str(entry))
                except (OSError, shutil.Error) as e:
                    failed_dirs.append(str(entry))
                    print(f"Error: Failed to remove directory {entry}: {e!s}")

        if removed_dirs:
            print(f"\nSuccessfully removed {len(removed_dirs)} test directories:")
            for dir_path in removed_dirs:
                print(f"- {dir_path}")

        if failed_dirs:
            print(f"\nFailed to remove {len(failed_dirs)} test directories:")
            for dir_path in failed_dirs:
                print(f"- {dir_path}")

    except Exception as e:
        print(f"Error: Unexpected error during cleanup: {e!s}")


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    """Cleanup test user directories after each test if it's the last test in the class."""
    if nextitem is None or nextitem.cls != item.cls:
        _cleanup_test_user_directories()


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """
    Cleanup test user libraries after test run completion.

    This function is called after the entire test suite has finished executing.
    It performs cleanup operations by removing test user library directories
    to ensure a clean state for subsequent test runs.

    Args:
        session: The pytest Session object containing test run information
        exitstatus: The exit status code of the test run

    Returns:
        None
    """
    print("Executing post-test cleanup operations...")
    _cleanup_test_user_directories()
    print("Cleanup complete.")


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    """Cleanup test user directories when pytest is unconfigured (e.g., on interruption)."""
    _cleanup_test_user_directories()
