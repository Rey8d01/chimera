"""Blog use cases."""

from utils.ca import UseCase, SuccessResponse
from .gateways import NewPostRequest, PostItemRequest


class PostItemUseCase(UseCase):
    """Сценарий для получения одного поста по определенному фильтру."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request_object: PostItemRequest) -> SuccessResponse:
        domain_post = await self.repository.get_item_post(filters=request_object.filters)
        return SuccessResponse(domain_post)


class NewPostUseCase(UseCase):
    """Сценарий для сохранения нового поста."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request_object: NewPostRequest) -> SuccessResponse:
        domain_post = await self.repository.create_post(doc=request_object.doc)
        return SuccessResponse(domain_post)
