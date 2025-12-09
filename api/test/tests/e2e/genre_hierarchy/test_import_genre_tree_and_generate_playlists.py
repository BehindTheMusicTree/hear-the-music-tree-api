import pytest
from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.serializer.model.criteria.input.tree_import.Fields import Fields as TreeImportFields
from api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from api.test.utils.AppTestCase import AppTestCase
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename


@pytest.mark.e2e
class TestCase(AppTestCase):
    """
    E2E test for genre tree import and automatic playlist generation.

    This test verifies the complete workflow:
    1. User authenticates
    2. User imports a complete genre tree via POST /genres/tree/import/
    3. System creates all genres with correct hierarchy
    4. User uploads multiple tracks and tags them with different genres
    5. System automatically creates playlists for all genres
    6. Tracks appear in correct playlists based on hierarchy
    """

    def test_import_genre_tree_and_generate_playlists_then_ok(self):
        from api.test.integration.view.criteria.GenreTestCase import GenreTestCase
        from api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase

        genre_test_case = GenreTestCase()
        genre_test_case.setUp()
        genre_test_case.api_client = self.api_client
        genre_test_case._login_as_test_user1()

        uploaded_track_test_case = UploadedTrackTestCase()
        uploaded_track_test_case.setUp()
        uploaded_track_test_case.api_client = self.api_client
        uploaded_track_test_case._login_as_test_user1()

        tree_data = [
            {
                TreeImportFields.NAME_PUBLIC: "Electronic Music",
                TreeImportFields.CHILDREN: [
                    {
                        TreeImportFields.NAME_PUBLIC: "Techno",
                        TreeImportFields.CHILDREN: [
                            {TreeImportFields.NAME_PUBLIC: "Minimal Techno", TreeImportFields.CHILDREN: []}
                        ]
                    },
                    {TreeImportFields.NAME_PUBLIC: "House", TreeImportFields.CHILDREN: []}
                ]
            },
            {
                TreeImportFields.NAME_PUBLIC: "Rock",
                TreeImportFields.CHILDREN: [
                    {TreeImportFields.NAME_PUBLIC: "Metal", TreeImportFields.CHILDREN: []}
                ]
            }
        ]

        response = genre_test_case._post_genres_tree_import(data={TreeImportFields.TREE: tree_data})
        assert response.status_code == status.HTTP_201_CREATED

        genres = Genre.objects.filter(user=self.test_user1)
        assert genres.count() == 6

        electronic = genres.get(name="Electronic Music")
        techno = genres.get(name="Techno")
        minimal_techno = genres.get(name="Minimal Techno")
        house = genres.get(name="House")
        rock = genres.get(name="Rock")
        metal = genres.get(name="Metal")

        assert electronic.parent is None
        assert techno.parent == electronic
        assert minimal_techno.parent == techno
        assert house.parent == electronic
        assert rock.parent is None
        assert metal.parent == rock

        playlists = CriteriaPlaylist.objects.filter(user=self.test_user1)
        assert playlists.count() == 6

        track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 1", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)
        track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 2", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)
        track3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 3", test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3)

        response = uploaded_track_test_case._put_uploaded_track(track1.uuid, **{PutFields.GENRE: "Minimal Techno"})
        assert response.status_code == status.HTTP_200_OK

        response = uploaded_track_test_case._put_uploaded_track(track2.uuid, **{PutFields.GENRE: "House"})
        assert response.status_code == status.HTTP_200_OK

        response = uploaded_track_test_case._put_uploaded_track(track3.uuid, **{PutFields.GENRE: "Metal"})
        assert response.status_code == status.HTTP_200_OK

        track1.refresh_from_db()
        track2.refresh_from_db()
        track3.refresh_from_db()

        track1_playlists = [p.uuid for p in track1.playlists.all()]
        track2_playlists = [p.uuid for p in track2.playlists.all()]
        track3_playlists = [p.uuid for p in track3.playlists.all()]

        minimal_techno_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=minimal_techno)
        techno_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=techno)
        electronic_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=electronic)
        house_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=house)
        metal_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=metal)
        rock_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock)

        assert len(track1_playlists) == 3
        assert minimal_techno_playlist.playlist.uuid in track1_playlists
        assert techno_playlist.playlist.uuid in track1_playlists
        assert electronic_playlist.playlist.uuid in track1_playlists

        assert len(track2_playlists) == 2
        assert house_playlist.playlist.uuid in track2_playlists
        assert electronic_playlist.playlist.uuid in track2_playlists

        assert len(track3_playlists) == 2
        assert metal_playlist.playlist.uuid in track3_playlists
        assert rock_playlist.playlist.uuid in track3_playlists

        assert track1 in electronic_playlist.playlist.uploaded_tracks.all()
        assert track2 in electronic_playlist.playlist.uploaded_tracks.all()
        assert track3 not in electronic_playlist.playlist.uploaded_tracks.all()
