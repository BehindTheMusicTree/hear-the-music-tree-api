import os
import shutil
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


def _should_mock_external_services(request) -> bool:
    """True when external services (OAuth, MusicBrainz, Spotify API) should be mocked: CI or non-e2e."""
    is_ci = os.environ.get("ENV") == "CI_TEST"
    is_e2e = request.node.get_closest_marker("e2e") or "/tests/e2e/" in str(request.fspath)
    return is_ci or not is_e2e


# External service mocks below use empty/minimal responses. Tests that need non-empty data
# (e.g. a recording, token, search results) should patch the same target and set return values.


@pytest.fixture(autouse=True)
def mock_oauth_outside_e2e(request):
    """Mock Spotify and Google OAuth at the view layer.

    - When ENV=CI_TEST: always mock for all tests, including e2e, so no real provider calls.
    - In dev (other ENV): mock only for non-e2e tests; e2e tests are not mocked so they can
      use real OAuth or their own mocks when run locally.
    """
    if _should_mock_external_services(request):
        with (
            patch("api.view.spotify_auth.SpotifyOAuthService"),
            patch("api.view.google_auth.GoogleOAuthService"),
        ):
            yield
    else:
        yield


@pytest.fixture(autouse=True)
def mock_musicbrainz_outside_e2e(request):
    """Mock AcoustID/MusicBrainz lookup so no real API calls are made.

    - When ENV=CI_TEST: always mock for all tests, including e2e.
    - In dev: mock only for non-e2e tests; e2e tests can use real lookup or their own mocks.
    """
    if _should_mock_external_services(request):
        with patch(
            "api.utils.musicbrainz.service.acoustid.lookup",
            return_value={"status": "ok", "results": []},
        ):
            yield
    else:
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

    - When ENV=CI_TEST: always mock for all tests, including e2e.
    - In dev: mock only for non-e2e tests; e2e tests can use real Spotify API or their own mocks.
    """
    if _should_mock_external_services(request):
        mock_instance = _make_spotify_client_mock()
        with (
            patch(
                "api.utils.spotify_api.managers.SpotifyApiLibTrackManager.SpotifyClient",
                return_value=mock_instance,
            ),
            patch(
                "api.utils.spotify_api.managers.SpotifyApiArtistManager.SpotifyClient",
                return_value=mock_instance,
            ),
            patch(
                "api.view.viewset.model.SpotifyArtistViewSet.SpotifyClient",
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
    """Run audio meta analysis path with mocked AFP in non-e2e tests; e2e tests use real AFP (e.g. in CI).

    - Non-e2e: override_settings(AFP_ENABLED=True) so the path runs regardless of
      .env; mock get_fingerprinting_result so no real AFP calls. Tests that need real AFP (e.g.
      critical AFP connection test) must use @pytest.mark.requires_real_afp to skip the AFP mock.
    - E2e: no override, no mock; e2e can use real AFP in CI.
    """
    is_e2e = _is_e2e(request)
    if is_e2e:
        yield
        return

    with override_settings(AFP_ENABLED=True):
        if request.node.get_closest_marker("requires_real_afp"):
            yield
        else:
            with patch(
                "api.utils.audio_fingerprinter.service.get_fingerprinting_result",
                return_value=_make_success_fingerprinting_result(),
            ):
                yield


critical_test_failed = False


IGNORED_TEST_DIRS = [
    'utils/',
]


def pytest_ignore_collect(collection_path: Path, config):
    str_path = str(collection_path)
    return any(ignored_dir in str_path for ignored_dir in IGNORED_TEST_DIRS)


def base_childinstance(request, db):
    test_case = request.param()
    test_case.setUp()
    yield test_case
    test_case.tearDown


def pytest_configure(config):
    config.addinivalue_line("markers", "critical: mark test as critical to pass")
    config.addinivalue_line("markers", "slow: mark test as long-running")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end (may require network or external services)")
    config.addinivalue_line(
        "markers",
        "requires_real_afp: skip AFP mock so the test calls the real audio fingerprinting service",
    )


def _run_has_e2e_tests(session: Session) -> bool:
    for item in session.items:
        if item.get_closest_marker("e2e") or "/tests/e2e/" in str(item.fspath):
            return True
    return False


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
        urllib.request.urlopen(req, timeout=E2E_REACHABILITY_TIMEOUT_SEC)
        return True, ""
    except Exception as e:
        return False, str(e) or type(e).__name__


def _check_spotify_reachable() -> tuple[bool, str]:
    return _check_url_reachable("https://accounts.spotify.com")


def _check_google_reachable() -> tuple[bool, str]:
    return _check_url_reachable("https://accounts.google.com")


def _check_musicbrainz_reachable() -> tuple[bool, str]:
    return _check_url_reachable("https://api.acoustid.org")


def pytest_collection_finish(session: Session) -> None:
    if not _run_has_e2e_tests(session):
        return
    is_ci = os.environ.get("ENV") == "CI_TEST"
    if is_ci:
        if not getattr(settings, "AFP_ENABLED", False):
            pytest.exit(
                "E2E tests require AFP. In CI (ENV=CI_TEST), AFP_ENABLED must be true.",
                returncode=2,
            )
        ok, reason = _check_afp_reachable()
        if not ok:
            pytest.exit(
                f"E2E tests require AFP. In CI (ENV=CI_TEST), the AFP service is unreachable. Reason: {reason}",
                returncode=2,
            )
        return
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
    if failures:
        pytest.exit(
            "E2E run requires all enabled services to be reachable. Unreachable: "
            + "; ".join(failures),
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
    if '/tests/critical/' in test_path:
        return 0
    elif '/tests/unit/' in test_path:
        return 1
    elif '/tests/integration/' in test_path:
        return 2
    elif '/tests/e2e/' in test_path:
        return 3
    else:
        return 4


def pytest_collection_modifyitems(config, items):
    # Order tests: critical marker first, then by directory (critical → unit → integration → e2e), slow marker last
    critical_tests = []
    normal_tests = []
    slow_tests = []

    print("Ordering tests: critical marker first, then by directory (tests/critical → tests/unit → tests/integration → tests/e2e), slow marker last")
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

    items[:] = critical_tests + normal_tests + slow_tests


@pytest.fixture()
def enable_audio_metadata_analysis(request):
    """Override audio meta analysis for this test via override_settings (inner override wins over autouse).

    Non-e2e tests get AFP_ENABLED=True and mocked AFP from mock_audio_meta_analysis_outside_e2e.
    Use this fixture with parametrize(..., [False], indirect=True) when a test needs the disabled path;
    request it in the test so override_settings(AFP_ENABLED=False) applies. E2e can request
    this fixture (default True) if needed.
    """
    enable = getattr(request, "param", True)
    with override_settings(AFP_ENABLED=enable):
        yield


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
                    print(f"Error: Failed to remove directory {entry}: {str(e)}")

        if removed_dirs:
            print(f"\nSuccessfully removed {len(removed_dirs)} test directories:")
            for dir_path in removed_dirs:
                print(f"- {dir_path}")

        if failed_dirs:
            print(f"\nFailed to remove {len(failed_dirs)} test directories:")
            for dir_path in failed_dirs:
                print(f"- {dir_path}")

    except Exception as e:
        print(f"Error: Unexpected error during cleanup: {str(e)}")


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
