"""Blog use cases."""

from utils.ca import UseCase, SuccessResponse, ErrorResponse, ResponseFromUseCase
from .gateways import CreatePostRequest, ItemPostRequest, UpdatePostRequest, ListPostsRequest, DeletePostRequest
from .domains import Post, PostMetaInfo, PostTag


class ItemPostUseCase(UseCase):
    """Сценарий для получения одного поста по определенному фильтру."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request: ItemPostRequest) -> ResponseFromUseCase:
        post = await self.repository.get_item_post(filters=request.filters)
        return SuccessResponse(post)


class ListPostsUseCase(UseCase):
    """Сценарий для получения списка постов по определенному фильтру."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request: ListPostsRequest) -> ResponseFromUseCase:
        list_posts = await self.repository.get_list_posts(
            alias_tag=request.filters.get("alias_tag"),
            user_id=request.filters.get("user_id"),
        )
        return SuccessResponse(list_posts)


class CreatePostUseCase(UseCase):
    """Сценарий для сохранения нового поста."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request: CreatePostRequest) -> ResponseFromUseCase:
        post = await self.repository.create_post(post=request.to_post())
        if not post:
            return ErrorResponse("error create")
        return SuccessResponse(post)


class UpdatePostUseCase(UseCase):
    """Сценарий для обновления поста."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request: UpdatePostRequest) -> ResponseFromUseCase:
        result = await self.repository.update_post(post=request.to_post())
        if not result:
            return ErrorResponse("error update")
        return SuccessResponse(result)


class DeletePostUseCase(UseCase):
    """Сценарий удаления поста."""

    def __init__(self, repository):
        self.repository = repository

    async def process_request(self, request: DeletePostRequest) -> ResponseFromUseCase:
        domain_post = await self.repository.delete_post(alias=request.alias)
        return SuccessResponse(domain_post)
