from hear.model.criteria.children.tag.Tag import Tag
from hear.view.viewset.model.criteria.CriteriaViewSet import CriteriaViewSet


class TagViewSet(CriteriaViewSet):
    def __init__(self, **kwargs):
        super().__init__(model_class=Tag, **kwargs)
