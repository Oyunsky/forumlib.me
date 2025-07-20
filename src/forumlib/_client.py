from __future__ import annotations

__all__ = ['ForumLib']

from typing import Optional

from . import enums
from ._types import ResponseT, IntOrStr
from ._models import Discussion, Category, Comment
from ._base_client import SyncAPIClient


class ForumLib(SyncAPIClient):
    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_endpoint: Optional[str] = None,
    ) -> None:
        if not base_url:
            base_url = 'https://forumlib.me'
        if not api_endpoint:
            api_endpoint = '/api/forum'
        super().__init__(base_url=base_url, api_endpoint=api_endpoint)

    def get_category(
        self,
        category: enums.Category = enums.Category.ALL,
        *,
        page: int = 1,
        sort: enums.Sort = enums.Sort.NEWEST
    ) -> Category:
        params = {'category': category.value, 'page': page, 'sort': sort.value}
        data = self.get('/discussion', params=params)
        return Category.parse(data) # type: ignore

    def get_discussion(self, discussion_id: IntOrStr) -> Discussion:
        data = self.get(f'/discussion/{discussion_id}')
        return Discussion.parse(data) # type: ignore

    def get_comments(self, discussion_id: IntOrStr, *, page: int = 1) -> Comment:
        params = {'discussion_id': discussion_id, 'page': page}
        data = self.get('/posts', params=params)
        return Comment.parse(data) # type: ignore