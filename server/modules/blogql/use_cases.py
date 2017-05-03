"""Blog use cases."""

from utils.ca import UseCase, SuccessResponse, ErrorResponse, ResponseFromUseCase
from .gateways import CreatePostRequest, ItemPostRequest, UpdatePostRequest, ListPostsRequest, DeletePostRequest
from .domains import Post, PostMetaInfo, PostTag


class ItemPostUseCase(UseCase):
    """Сценарий для получения одного поста по определенному фильтру."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request_object: ItemPostRequest) -> ResponseFromUseCase:
        post = await self.repository.get_item_post(filters=request_object.filters)
        return SuccessResponse(post)


class ListPostsUseCase(UseCase):
    """Сценарий для получения списка постов по определенному фильтру."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request_object: ListPostsRequest) -> ResponseFromUseCase:
        list_posts = await self.repository.get_list_posts(
            alias_tag=request_object.filters.get("alias_tag"),
            user_id=request_object.filters.get("user_id"),
        )
        return SuccessResponse(list_posts)


class CreatePostUseCase(UseCase):
    """Сценарий для сохранения нового поста."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request_object: CreatePostRequest) -> ResponseFromUseCase:
        post = await self.repository.create_post(post=request_object.to_post())
        if not post:
            return ErrorResponse("error create")
        return SuccessResponse(post)


class UpdatePostUseCase(UseCase):
    """Сценарий для обновления поста."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request_object: UpdatePostRequest) -> ResponseFromUseCase:
        result = await self.repository.update_post(post=request_object.to_post())
        if not result:
            return ErrorResponse("error update")
        return SuccessResponse(result)


class DeletePostUseCase(UseCase):
    """Сценарий удаления поста."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request_object: DeletePostRequest) -> ResponseFromUseCase:
        domain_post = await self.repository.delete_post(alias=request_object.alias)
        return SuccessResponse(domain_post)
