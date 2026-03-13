from rest_framework import status

from api.model.criteria.children.genre.Genre import Genre
from api.model.uploaded_track.UploadedTrack import UploadedTrack
from api.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as UploadedTrackFields
from api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from api.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestWithExistingTracks(GenreTestCase):

    def test_load_example_tree_with_existing_tracks_then_tracks_genres_nullified(self):
        # Create existing genres
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)

        # Create uploaded tracks with genres
        track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 1",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            user=self.test_user1,
            **{UploadedTrackFields.GENRE.value: genre_rock}
        )
        track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 2",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            user=self.test_user1,
            **{UploadedTrackFields.GENRE.value: genre_metal}
        )

        # Verify tracks have genres before loading example tree
        track1.refresh_from_db()
        track2.refresh_from_db()
        assert track1.genre == genre_rock
        assert track2.genre == genre_metal

        # Load example tree
        response = self._post_genres_tree_load_example()

        # Verify successful response
        assert response.status_code == status.HTTP_201_CREATED

        # Verify tracks have null genres after loading example tree
        track1.refresh_from_db()
        track2.refresh_from_db()
        assert track1.genre is None
        assert track2.genre is None

        # Verify old genres are deleted and new example tree is loaded
        # The old "Rock" and "Metal" genres should be deleted, but new ones from example tree should exist
        old_rock_count = Genre.objects.filter(user=self.test_user1, name="Rock").count()
        old_metal_count = Genre.objects.filter(user=self.test_user1, name="Metal").count()
        # Should have new example tree genres (not the old ones we created)
        assert old_rock_count > 0  # New example tree has "Rock"
        assert old_metal_count > 0  # New example tree has "Metal"
        # Verify example tree genres are loaded (checking for some expected genres from the example tree)
        assert Genre.objects.filter(user=self.test_user1, name="Electronic").count() > 0
        assert Genre.objects.filter(user=self.test_user1, name="Jazz").count() > 0

    def test_load_example_tree_with_tracks_from_different_user_then_only_current_user_tracks_affected(self):
        # Create genres for both users
        genre_rock_user1 = self.model_fixture_factory.create_genre(name="Rock", user=self.test_user1)
        genre_rock_user2 = self.model_fixture_factory.create_genre(name="Rock", user=self.test_user2)

        # Create tracks for both users
        track1_user1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 1 User 1",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            user=self.test_user1,
            **{UploadedTrackFields.GENRE.value: genre_rock_user1}
        )
        track2_user2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Track 2 User 2",
            test_uploaded_track_filename=UploadedTrackTestFilename.DEFAULT_MP3,
            user=self.test_user2,
            **{UploadedTrackFields.GENRE.value: genre_rock_user2}
        )

        # Load example tree as user1
        response = self._post_genres_tree_load_example()

        # Verify successful response
        assert response.status_code == status.HTTP_201_CREATED

        # Verify only user1's track has null genre
        track1_user1.refresh_from_db()
        track2_user2.refresh_from_db()
        assert track1_user1.genre is None
        assert track2_user2.genre == genre_rock_user2

        # Verify only user1's genre is deleted and example tree is loaded
        # User1 should have new example tree genres (not the old ones we created)
        user1_rock_count = Genre.objects.filter(user=self.test_user1, name="Rock").count()
        user2_rock_count = Genre.objects.filter(user=self.test_user2, name="Rock").count()
        assert user1_rock_count > 0  # New example tree has "Rock" for user1
        assert user2_rock_count == 1  # User2 still has old "Rock" genre
        # Verify reference tree genres are loaded for user1
        assert Genre.objects.filter(user=self.test_user1, name="Electronic").count() > 0
        assert Genre.objects.filter(user=self.test_user1, name="Jazz").count() > 0

    def test_load_example_tree_with_no_existing_tracks_then_success(self):
        # Load example tree with no existing tracks
        response = self._post_genres_tree_load_example()

        # Verify successful response
        assert response.status_code == status.HTTP_201_CREATED

        # Verify no tracks exist
        assert UploadedTrack.objects.filter(user=self.test_user1).count() == 0
