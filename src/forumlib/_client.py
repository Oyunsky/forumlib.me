from __future__ import annotations

__all__ = ['ForumLib']

from typing import Optional

from .enums import Category, Sort
from ._types import ResponseT, IntOrStr
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
        category: Category = Category.ALL,
        *,
        page: int = 1,
        sort: Sort = Sort.NEWEST
    ) -> ResponseT:
        params = {'category': category.value, 'page': page, 'sort': sort.value}
        return self.get('/discussion', params=params)

    def get_discussion(self, discussion_id: IntOrStr) -> ResponseT:
        return self.get(f'/discussion/{discussion_id}')

    def get_comments(self, discussion_id: IntOrStr, *, page: int = 1) -> ResponseT:
        params = {'discussion_id': discussion_id, 'page': page}
        return self.get('/posts', params=params)