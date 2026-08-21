from rest_framework import status

from api.model.playlist.children.criteria.tag.TagPlaylist import TagPlaylist
from api.model.playlist.Playlist import Playlist
from api.model.track_playlist_rel.TrackPlaylistRel import TrackPlaylistRel
from api.test.tests.integration.criteria.TagTestCase import TagTestCase


class TestCase(TagTestCase):
    def test_delete_root_criteria_with_children_then_direct_tracks_in_criterialess_playlist_in_first_positions(self):
        tagless_criteria_playlist = TagPlaylist.objects.get(user=self.test_user1, criteria=None)

        tagless_uploaded_track_added_first = self.model_fixture_factory.create_uploaded_track_with_file(
            title="tagless first"
        )
        TrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=tagless_criteria_playlist, track=tagless_uploaded_track_added_first
        )
        tagless_uploaded_track_added_second = self.model_fixture_factory.create_uploaded_track_with_file(
            title="tagless second"
        )
        TrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=tagless_criteria_playlist, track=tagless_uploaded_track_added_second
        )

        party_criteria = self.model_fixture_factory.create_tag(name="party")
        fiesta_criteria = self.model_fixture_factory.create_tag(name="fiesta", parent=party_criteria)

        party_uploaded_track_added_third = self.model_fixture_factory.create_uploaded_track_with_file(
            title="party third"
        )
        TrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=party_criteria.criteria_playlist, track=party_uploaded_track_added_third
        )
        fiesta_uploaded_track_added_fourth = self.model_fixture_factory.create_uploaded_track_with_file(
            title="fiesta fourth"
        )
        TrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=fiesta_criteria.criteria_playlist, track=fiesta_uploaded_track_added_fourth
        )
        party_uploaded_track_added_fifth = self.model_fixture_factory.create_uploaded_track_with_file(
            title="party fifth"
        )
        TrackPlaylistRel.objects.create(
            user=self.test_user1, playlist=party_criteria.criteria_playlist, track=party_uploaded_track_added_fifth
        )

        response = self._delete_tag(uuid=party_criteria.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not TagPlaylist.objects.filter(criteria=party_criteria).exists()
        assert TagPlaylist.objects.filter(criteria=fiesta_criteria).exists()
        fiesta_playlist = TagPlaylist.objects.get(criteria=fiesta_criteria)
        assert fiesta_playlist.uploaded_tracks_not_archived_dict_by_position[1].uuid == (
            fiesta_uploaded_track_added_fourth.uuid
        )

        tagless_playlist: Playlist = TagPlaylist.objects.get(user=self.test_user1, criteria=None)
        uploaded_tracks_dict_by_position = tagless_playlist.uploaded_tracks_not_archived_dict_by_position
        assert len(uploaded_tracks_dict_by_position) == 4
        assert uploaded_tracks_dict_by_position[1].uuid == party_uploaded_track_added_fifth.uuid
        assert uploaded_tracks_dict_by_position[2].uuid == party_uploaded_track_added_third.uuid
        assert uploaded_tracks_dict_by_position[3].uuid == tagless_uploaded_track_added_second.uuid
        assert uploaded_tracks_dict_by_position[4].uuid == tagless_uploaded_track_added_first.uuid
