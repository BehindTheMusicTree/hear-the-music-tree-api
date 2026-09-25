from hear.model.criteria.children.genre.Genre import Genre
from hear.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet


class GenreViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=Genre, **kwargs)
