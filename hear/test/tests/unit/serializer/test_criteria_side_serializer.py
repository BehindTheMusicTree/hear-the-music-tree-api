from hear.serializer.model.criteria.output.CriteriaOutputFieldKey import CriteriaOutputFieldKey
from hear.serializer.model.criteria.output.detailed import CriteriaDetailedSerializer
from hear.serializer.model.criteria.output.simple import CriteriaSimpleSerializer
from hear.test.tests.integration.criteria.GenreTestCase import GenreTestCase


class TestCriteriaSideSerializer(GenreTestCase):
    """
    `side` lives only on the concrete `Genre` MTI subtype, not on the shared `Criteria`
    table these serializers are built against (`Meta.model = Criteria`, shared by both
    `GenreViewSet` and `TagViewSet`). Serializing a genre through the API always passes a
    concrete `Genre` instance (see `AppModelViewSet.get_object`/`get_queryset`, which query
    via `model_class.objects`), so that path never actually exercises the base-`Criteria`
    resolution -- these tests reproduce it directly by serializing `genre.criteria_ptr`,
    the base `Criteria` row itself, mirroring the kit's own
    `test_criteria_simple_serializer_resolves_side_from_genre_mti_subtype`.
    """

    def test_simple_serializer_base_criteria_ptr_of_genre_then_resolves_side_from_mti_subtype(self):
        side = "core"
        genre = self.model_fixture_factory.create_genre(name="rock", side=side)

        data = CriteriaSimpleSerializer(genre.criteria_ptr).data

        assert data[CriteriaOutputFieldKey.SIDE.value] == side

    def test_simple_serializer_base_criteria_ptr_of_tag_then_side_is_none(self):
        tag = self.model_fixture_factory.create_tag(name="live")

        data = CriteriaSimpleSerializer(tag.criteria_ptr).data

        assert data[CriteriaOutputFieldKey.SIDE.value] is None

    def test_detailed_serializer_base_criteria_ptr_of_genre_then_resolves_side_from_mti_subtype(self):
        side = "core"
        genre = self.model_fixture_factory.create_genre(name="rock", side=side)

        data = CriteriaDetailedSerializer(genre.criteria_ptr).data

        assert data[CriteriaOutputFieldKey.SIDE.value] == side

    def test_detailed_serializer_base_criteria_ptr_of_tag_then_side_is_none(self):
        tag = self.model_fixture_factory.create_tag(name="live")

        data = CriteriaDetailedSerializer(tag.criteria_ptr).data

        assert data[CriteriaOutputFieldKey.SIDE.value] is None
