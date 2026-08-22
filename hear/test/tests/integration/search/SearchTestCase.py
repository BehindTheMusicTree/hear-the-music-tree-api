from typing import Any

from django.urls import reverse

from hear.test.utils.AppTestCase import AppTestCase


class SearchMixin:
    """Mixin that adds search API helpers. Use with any AppTestCase subclass for E2E tests that need search."""

    api_client: Any
    _set_results: Any

    def _search(self, **kwargs):
        return self.api_client.get(path=reverse("search-list"), data=kwargs, handle_response=self._set_results)

    def _post_search(self, **kwargs):
        return self.api_client.post(
            path=reverse("search-list"), data=kwargs, content_type="application/json", handle_response=self._set_results
        )

    def _put_search(self, **kwargs):
        return self.api_client.put(
            path=reverse("search-list"), data=kwargs, content_type="application/json", handle_response=self._set_results
        )


class SearchTestCase(SearchMixin, AppTestCase):
    pass
