from uuid import UUID

from django.urls import reverse

from hear.model.album.Album import Album
from hear.test.utils.AppTestCase import AppTestCase


class AlbumTestCase(AppTestCase[Album]):
    saved_object: Album
    model_class = Album

    def _post_album(self, **kwargs):
        return self.api_client.post(
            path=reverse("me-album-list"),
            data=kwargs,
            content_type="application/json",
            handle_response=self._set_results,
        )

    def _list_albums(self, **kwargs):
        return self.api_client.get(path=reverse("me-album-list"), data=kwargs, handle_response=self._set_results)

    def _retrieve_album(self, uuid: UUID):
        return self.api_client.get(
            path=reverse("me-album-detail", kwargs={"pk": uuid}), handle_response=self._set_results
        )

    def _put_album(self, uuid: UUID, **kwargs):
        return self.api_client.put(
            path=reverse("me-album-detail", kwargs={"pk": uuid}),
            data=kwargs,
            content_type="application/json",
            handle_response=self._set_results,
        )

    def _delete_album(self, uuid: UUID):
        return self.api_client.delete(path=reverse("me-album-detail", kwargs={"pk": uuid}))
