from uuid import UUID

from django.db import models
from django.urls import reverse
from rest_framework import status
from the_music_tree_api_kit.view.pagination.PaginatedResponseFields import PaginatedResponseFields

from api.model.criteria.children.tag.Tag import Tag
from api.test.tests.integration.reference.reference_test_case import ReferenceTestCase


class ReferenceTagTestCase(ReferenceTestCase):
    def test_reference_tag_list_then_200(self):
        self.model_fixture_factory.create_tag("tmta_tag", user=self._system_user)
        self.model_fixture_factory.create_tag("user1_tag", user=self.test_user1)
        response = self.api_client.get(path=reverse("reference-tag-list"))
        self._assert_all_results_belong_to_tmta(response, Tag)
