import zlib
from uuid import UUID

from django.urls import reverse

from hear.model.criteria.children.genre.Genre import Genre
from hear.serializer.model.criteria.input.tree_import import Fields
from hear.test.utils.AppTestCase import AppTestCase


def _set_missing_node_ids(nodes, used_ids=None):
    """Name-derived Wikidata-style ids keep the pre-0.28 name-matching semantics tests were written against. Ids stay
    unique so duplicate-name validation, not duplicate-id validation, is what repeated names trip."""
    if used_ids is None:
        used_ids = set()
    if not isinstance(nodes, list):
        return
    for node in nodes:
        if not isinstance(node, dict):
            continue
        name = node.get(Fields.NAME_PUBLIC)
        if Fields.ID not in node and isinstance(name, str) and name:
            node_id = f"Q{zlib.crc32(name.encode())}"
            while node_id in used_ids:
                node_id += "0"
            node[Fields.ID] = node_id
        used_ids.add(node.get(Fields.ID))
        _set_missing_node_ids(node.get(Fields.CHILDREN), used_ids)


class GenreTestCase(AppTestCase[Genre]):
    saved_object: Genre
    model_class = Genre

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detail_endpoint = "me-genre-detail"
        self.list_endpoint = "me-genre-list"

    def _retrieve_genre(self, uuid: UUID):
        return self.api_client.get(
            path=reverse(self.detail_endpoint, kwargs={"pk": uuid}), handle_response=self._set_results
        )

    def _list_genres(self, **kwargs):
        return self.api_client.get(path=reverse(self.list_endpoint), data=kwargs, handle_response=self._set_results)

    def _get_genres_tree(self, allows_multiple_primary_parents: bool = False):
        return self.api_client.get(
            path=reverse(self.list_endpoint) + "tree/",
            data={Fields.ALLOWS_MULTIPLE_PRIMARY_PARENTS: str(allows_multiple_primary_parents).lower()},
            handle_response=self._set_error_response_result_if_failure,
        )

    def _post_genre(self, **kwargs):
        return self.api_client.post(
            path=reverse(self.list_endpoint),
            data=kwargs,
            content_type="application/json",
            handle_response=self._set_results,
        )

    def _post_genre_with_duplicate_fields(self, raw_json: str):
        return self.api_client.post(
            path=reverse(self.list_endpoint),
            data=raw_json,
            content_type="application/json",
            handle_response=self._set_results,
        )

    def _put_genre(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse(self.detail_endpoint, kwargs={"pk": uuid}),
            data=kwargs,
            content_type="application/json",
            handle_response=self._set_results,
        )

    def _put_genre_with_duplicate_fields(self, uuid: UUID, raw_json: str):
        return self.api_client.put(
            path=reverse(self.detail_endpoint, kwargs={"pk": uuid}),
            data=raw_json,
            content_type="application/json",
            handle_response=self._set_results,
        )

    def _delete_genre(self, uuid: UUID):
        return self.api_client.delete(path=reverse(self.detail_endpoint, kwargs={"pk": uuid}))

    def _post_genres_tree_import(self, data=None):
        if isinstance(data, dict) and Fields.TREE in data:
            data = {Fields.ALLOWS_MULTIPLE_PRIMARY_PARENTS: False, **data}
            _set_missing_node_ids(data[Fields.TREE])
        return self.api_client.post(
            path=reverse(self.list_endpoint) + "tree/import/",
            data=data,
            content_type="application/json",
            handle_response=self._set_results,
        )
