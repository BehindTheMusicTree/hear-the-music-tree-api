from the_music_tree_genre_kit.view.viewset.genre.GenreExampleTreeMixin import GenreExampleTreeMixin

from api.model.criteria.children.genre.Genre import Genre
from api.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet


class GenreViewSet(GenreExampleTreeMixin[Genre], CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=Genre, **kwargs)

    def on_example_tree_loaded(self, request) -> None:
        from api.model.uploaded_track.UploadedTrack import UploadedTrack
        from api.model.uploaded_track.UploadedTrackFieldKey import UploadedTrackFieldKey as UploadedTrackFields

        UploadedTrack.objects.filter(user=request.user).update(**{UploadedTrackFields.GENRE.value: None})
