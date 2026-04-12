from datetime import timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import status

from api.model.play.Play import Play
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.play.input.schema.PostFields import Fields as PlayPostFields
from api.test.tests.integration.play.PlayTestCase import PlayTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.utils.data_transformer import to_camel_case


@pytest.mark.e2e
class TestCase(PlayTestCase):
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
            title="Track 1", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )
        track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 2", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )
        track3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 3", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3
        )

        response = self._post_play(**{to_camel_case(PlayPostFields.CONTENT): str(track1.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play1 = self.saved_object

        response = self._post_play(**{to_camel_case(PlayPostFields.CONTENT): str(track2.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play2 = self.saved_object

        response = self._post_play(**{to_camel_case(PlayPostFields.CONTENT): str(track1.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play3 = self.saved_object

        response = self._post_play(**{to_camel_case(PlayPostFields.CONTENT): str(track3.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        play4 = self.saved_object

        response = self._get_plays()
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 4

        plays = Play.objects.filter(user=self.test_user1)
        assert plays.count() >= 4

        track_ct = ContentType.objects.get_for_model(UploadedTrack)
        track1_plays = plays.filter(content_type=track_ct, content_uuid=track1.uuid)
        track2_plays = plays.filter(content_type=track_ct, content_uuid=track2.uuid)
        track3_plays = plays.filter(content_type=track_ct, content_uuid=track3.uuid)

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

        response = self._get_plays(
            **{
                to_camel_case("created_on_gte"): past_date,
                to_camel_case("created_on_lte"): future_date,
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total >= 4
