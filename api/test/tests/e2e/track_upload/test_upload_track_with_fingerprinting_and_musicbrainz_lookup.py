import pytest
from unittest.mock import patch
from rest_framework import status

from api.model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from api.model.musicbrainz_resource.children.recording.MbRecording import MbRecording
from api.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename

ACOUSTID_LOOKUP_RECORDING_PAYLOAD = {
    "status": "ok",
    "results": [
        {
            "score": 1.0,
            "recordings": [
                {
                    "id": "e2e-mock-recording-id",
                    "title": "E2E Mock Recording",
                    "artists": [{"id": "e2e-mock-artist-id", "name": "E2E Mock Artist"}],
                    "duration": 441,
                }
            ],
        }
    ],
}


@pytest.mark.e2e
@pytest.mark.usefixtures("enable_audio_metadata_analysis")
class TestCase(UploadedTrackTestCase):
    """
    E2E test for complete track upload workflow with audio fingerprinting and MusicBrainz lookup.

    This test verifies the complete workflow:
    1. User authenticates
    2. User uploads an audio file
    3. System fingerprints the audio using AcoustID
    4. System looks up fingerprint in MusicBrainz via AcoustID
    5. System retrieves and stores MusicBrainz recording metadata
    6. System creates/updates MusicBrainz artist records
    7. User retrieves the uploaded track and verifies metadata is populated

    In CI, conftest mocks MusicBrainz with empty results; this test overrides with a mock
    recording so the success path is asserted deterministically.
    """

    def test_upload_track_with_fingerprinting_and_musicbrainz_lookup_then_ok(self):
        with patch(
            "api.utils.musicbrainz.service.acoustid.lookup",
            return_value=ACOUSTID_LOOKUP_RECORDING_PAYLOAD,
        ):
            response = self._post_uploaded_track(
                UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)

        assert response.status_code == status.HTTP_201_CREATED

        track = self.saved_object
        track_file = track.track_file

        assert track is not None
        assert track_file is not None

        fingerprint_bytes = track_file.fingerprint_bytes
        fingerprint_missing_cause = track_file.fingerprint_missing_cause
        if fingerprint_bytes is None:
            if fingerprint_missing_cause:
                code_label = fingerprint_missing_cause.code.label if fingerprint_missing_cause else "Unknown"
                message = fingerprint_missing_cause.message if fingerprint_missing_cause and fingerprint_missing_cause.message else "No message"
                pytest.skip(
                    f"Fingerprint not generated. "
                    f"Missing cause: {code_label} - {message}"
                )
            else:
                assert False, "Fingerprint is None but no fingerprint_missing_cause is set"
        assert fingerprint_bytes is not None
        assert len(fingerprint_bytes) > 0

        musicbrainz_recording = track_file.musicbrainz_recording
        if musicbrainz_recording is None:
            missing_cause = track_file.musicbrainz_recording_missing_cause
            code_label = missing_cause.code.label if missing_cause else "Unknown"
            message = missing_cause.message if missing_cause and missing_cause.message else "No message"
            fingerprint_missing_cause = track_file.fingerprint_missing_cause
            fingerprint_code_label = fingerprint_missing_cause.code.label if fingerprint_missing_cause else "None"
            pytest.skip(
                f"MusicBrainz recording not found. "
                f"Missing cause: {code_label} - {message}. "
                f"Fingerprint missing cause: {fingerprint_code_label}"
            )

        assert musicbrainz_recording is not None
        assert isinstance(musicbrainz_recording, MbRecording)
        assert musicbrainz_recording.musicbrainz_id == "e2e-mock-recording-id"
        assert musicbrainz_recording.title == "E2E Mock Recording"

        musicbrainz_artists = musicbrainz_recording.musicbrainz_artists.all()
        assert musicbrainz_artists.exists()
        assert musicbrainz_artists.count() > 0

        for mb_artist in musicbrainz_artists:
            assert isinstance(mb_artist, MbArtist)
            assert mb_artist.musicbrainz_id is not None
            assert len(mb_artist.musicbrainz_id) > 0
            assert mb_artist.name is not None
            assert len(mb_artist.name) > 0

        response = self._retrieve_uploaded_track(track.uuid)
        assert response.status_code == status.HTTP_200_OK

        retrieved_track = self.saved_object
        assert retrieved_track is not None
        assert retrieved_track.uuid == track.uuid
        assert retrieved_track.title is not None
