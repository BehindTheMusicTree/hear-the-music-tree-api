from django.urls import reverse
from rest_framework import status

from api.serializer.audio_metadata.Fields import Fields
from api.test.tests.integration.audio_metadata.AudioMetadataTestCase import AudioMetadataTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


def _post_metadata_session(client, test_uploaded_track_filename: UploadedTrackTestFilename, **kwargs):
    file_abs_path = AudioMetadataTestCase.TEST_FILES_BASE_DIR / test_uploaded_track_filename.value
    with open(file_abs_path, "rb") as sample_file:
        data = {Fields.FILE: sample_file, **kwargs}
        return client.post(
            path=reverse("audio-metadata-session"),
            data=data,
            format="multipart",
        )


class TestMetadataSessionUpload(AudioMetadataTestCase):
    def test_upload_then_200_and_metadata_plus_session_token(self):
        response = _post_metadata_session(
            self.api_client,
            UploadedTrackTestFilename.DEFAULT_MP3,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "sessionToken" in data or "session_token" in data
        assert "sessionExpiresInSeconds" in data or "session_expires_in_seconds" in data
        session_token = data.get("sessionToken") or data.get("session_token")
        session_expires = data.get("sessionExpiresInSeconds") or data.get("session_expires_in_seconds")
        assert session_token
        assert session_expires == 900

    def test_upload_then_download_with_metadata_then_200_and_file(self):
        response = _post_metadata_session(
            self.api_client,
            UploadedTrackTestFilename.DEFAULT_MP3,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        token = data.get("sessionToken") or data.get("session_token")
        assert token
        download_response = self.api_client.post(
            path=reverse("audio-metadata-session-download"),
            data={"title": "Updated Title", "artists_names": ["New Artist"]},
            format="json",
            HTTP_X_SESSION_TOKEN=token,
        )
        assert download_response.status_code == status.HTTP_200_OK
        content_disposition = download_response.get("Content-Disposition")
        assert content_disposition is not None
        assert "attachment" in content_disposition
        assert "filename=" in content_disposition
        assert "filename*=" in content_disposition
        expose_headers = download_response.get("Access-Control-Expose-Headers")
        assert expose_headers is not None
        exposed_headers = [header.strip().lower() for header in expose_headers.split(",")]
        assert "content-disposition" in exposed_headers
        assert download_response.get("Content-Type") == "audio/mpeg"

    def test_download_without_token_then_400(self):
        response = self.api_client.post(
            path=reverse("audio-metadata-session-download"),
            data={},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_download_with_invalid_token_then_410(self):
        response = self.api_client.post(
            path=reverse("audio-metadata-session-download"),
            data={"session_token": "nonexistenttoken123"},
            format="json",
        )
        assert response.status_code == status.HTTP_410_GONE

    def test_upload_then_download_twice_with_different_metadata_then_both_200(self):
        response = _post_metadata_session(
            self.api_client,
            UploadedTrackTestFilename.DEFAULT_MP3,
        )
        assert response.status_code == status.HTTP_200_OK
        token = response.json().get("sessionToken") or response.json().get("session_token")
        assert token
        r1 = self.api_client.post(
            path=reverse("audio-metadata-session-download"),
            data={"title": "First"},
            format="json",
            HTTP_X_SESSION_TOKEN=token,
        )
        assert r1.status_code == status.HTTP_200_OK
        r2 = self.api_client.post(
            path=reverse("audio-metadata-session-download"),
            data={"title": "Second"},
            format="json",
            HTTP_X_SESSION_TOKEN=token,
        )
        assert r2.status_code == status.HTTP_200_OK
