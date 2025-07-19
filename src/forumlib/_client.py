from .enums import Category, Sort
from ._base_client import SyncAPIClient


class ForumLib(SyncAPIClient):
    def __init__(self, *, base_url=None, api_endpoint=None):
        if not base_url:
            base_url = 'https://forumlib.me'
        if not api_endpoint:
            api_endpoint = '/api/forum'
        super().__init__(base_url=base_url, api_endpoint=api_endpoint)

    def get_category(self, category=Category.ВСЕ, *, page=1, sort=Sort.НОВЫЕ):
        params = {'category': category.value, 'page': page, 'sort': sort.value}
        return self.get('/discussion', params=params)

    def get_discussion(self, discussion_id):
        return self.get(f'/discussion/{discussion_id}')

    def get_comments(self, discussion_id, *, page=1):
        params = {'discussion_id': discussion_id, 'page': page}
        return self.get('/posts', params=params)