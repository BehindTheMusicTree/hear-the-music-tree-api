import pytest

from api.test.tests import conftest
from api.test.tests.integration.uploaded_track.input.update_file_metadata.album_artists.TestCase import (
    FlacTestCase,
    Mp3TestCase,
    WavTestCase,
)


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)
