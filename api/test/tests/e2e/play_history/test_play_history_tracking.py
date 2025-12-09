import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework import status

from api.model.play.Play import Play
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.play.input.schema.PostFields import Fields as PlayPostFields
from api.test.integration.view.play.PlayTestCase import PlayTestCase
from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(PlayTestCase, UploadedTrackTestCase):
    """
    E2E test for complete play history tracking.

    This test verifies the complete workflow:
    1. User authenticates
    2. User uploads multiple tracks
    3. User records plays for different tracks at different times
    4. User retrieves play history
    5. User filters play history by date range
    6. User verifies play counts are tracked correctly
    """

    def test_play_history_tracking_then_ok(self):
        track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 1", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)
        track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 2", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)
        track3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 3", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)

        response = self._post_play(**{PlayPostFields.UPLOADED_TRACK: str(track1.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play1 = self.saved_object

        response = self._post_play(**{PlayPostFields.UPLOADED_TRACK: str(track2.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play2 = self.saved_object

        response = self._post_play(**{PlayPostFields.UPLOADED_TRACK: str(track1.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play3 = self.saved_object

        response = self._post_play(**{PlayPostFields.UPLOADED_TRACK: str(track3.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play4 = self.saved_object

        response = self._get_plays()
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 4

        plays = Play.objects.filter(user=self.test_user1)
        assert plays.count() >= 4

        track1_plays = plays.filter(uploaded_track=track1)
        track2_plays = plays.filter(uploaded_track=track2)
        track3_plays = plays.filter(uploaded_track=track3)

        assert track1_plays.count() >= 2
        assert track2_plays.count() >= 1
        assert track3_plays.count() >= 1

        track1.refresh_from_db()
        track2.refresh_from_db()
        track3.refresh_from_db()

        assert track1.play_count >= 2
        assert track2.play_count >= 1
        assert track3.play_count >= 1

        now = timezone.now()
        past_date = (now - timedelta(days=1)).isoformat()
        future_date = (now + timedelta(days=1)).isoformat()

        response = self._get_plays(**{'created_on__gte': past_date, 'created_on__lte': future_date})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 4
