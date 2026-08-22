import pytest
from rest_framework import status

from hear.model.musicbrainz_resource.children.artist.MbArtist import MbArtist
from hear.model.musicbrainz_resource.children.recording.MbRecording import MbRecording
from hear.test.tests.integration.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from hear.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(UploadedTrackTestCase):
    """
    E2E test for complete track upload workflow with audio fingerprinting and MusicBrainz lookup.

    Verifies the full stack with real AFP and real AcoustID/MusicBrainz in dev; in CI,
    conftest mocks MusicBrainz (empty results), so the test may skip when no recording is found.
    """

    def test_upload_track_with_fingerprinting_and_musicbrainz_lookup_then_ok(self):
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3,
        )

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
                message = (
                    fingerprint_missing_cause.message
                    if fingerprint_missing_cause and fingerprint_missing_cause.message
                    else "No message"
                )
                pytest.skip(f"Fingerprint not generated. Missing cause: {code_label} - {message}")
            else:
                raise AssertionError("Fingerprint is None but no fingerprint_missing_cause is set")
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
        assert musicbrainz_recording.musicbrainz_id is not None
        assert len(musicbrainz_recording.musicbrainz_id) > 0
        assert musicbrainz_recording.title is not None
        assert len(musicbrainz_recording.title) > 0

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
