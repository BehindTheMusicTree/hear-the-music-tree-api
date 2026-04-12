from django.urls import reverse

from api.model.playlist.children.criteria.tag.TagPlaylist import TagPlaylist
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase


class ReferenceTagPlaylistTestCase(ReferenceTestCase):
    def test_reference_tag_playlist_list_then_200(self):
        # Create a tag, which should create a playlist
        self.model_fixture_factory.create_tag("tmta_tag", user=self._system_user)
        response = self.api_client.get(path=reverse("reference-tag-playlist-list"))
        self._assert_all_results_belong_to_tmta(response, TagPlaylist)

    def test_reference_tag_playlist_retrieve_then_200(self):
        tag = self.model_fixture_factory.create_tag("tmta_tag", user=self._system_user)
        # Find the playlist for this tag
        playlist = TagPlaylist.objects.get(criteria=tag)
        response = self.api_client.get(path=reverse("reference-tag-playlist-detail", kwargs={"pk": playlist.uuid}))
        self._assert_retrieve_result_belongs_to_tmta(response, TagPlaylist)
