import pytest

from hear.test.tests import conftest
from hear.test.tests.integration.uploaded_track.input.update_file_metadata.album.TestCase import (
    FlacTestCase,
    Mp3TestCase,
    WavTestCase,
)


@pytest.fixture(params=[Mp3TestCase, WavTestCase, FlacTestCase])
def childinstance(request, db):
    yield from conftest.base_childinstance(request, db)
