from enum import Enum

import httpx


class Category(str, Enum):
    ВСЕ = 'all'
    БАГИ_И_ПРОБЛЕМЫ = '1'
    ПРЕДЛОЖЕНИЯ_ДЛЯ_САЙТА = '2'
    ПОИСК_ТАЙТЛОВ = '3'
    ПОИСК_КАДРОВ = '4'
    ОБСУЖДЕНИЕ_МАНГИ = '5'
    ОБСУЖДЕНИЕ_АНИМЕ = '6'
    ОБСУЖДЕНИЕ_РАНОБЭ = '7'
    ВИДЕОИГРЫ = '8'
    ПЕРЕВОДЧИКАМ = '9'
    КАК_ПЕРЕВОДИТЬ_МАНГУ = '10'
    КАК_РИСОВАТЬ_МАНГУ = '11'
    ОБЩЕНИЕ = '12'
    ДРУГОЕ = '13'


class Sort(str, Enum):
    НОВЫЕ = 'newest'
    ПО_ОБНОВЛЕНИЮ = 'updates'
    ОБСУЖДАЕМЫЕ = 'popular'


class Options:
    __slots__ = ('method', 'path', 'params')

    def __init__(self, method, path, *, params=None):
        self.method = method
        self.path = path
        self.params = params

    @classmethod
    def get(cls, path, *, params=None):
        return cls('GET', path, params=params)


class BaseClient:
    __slots__ = ('_base_url', '_api_endpoint')
    _client = None

    def __init__(self, *, base_url, api_endpoint):
        self._base_url = base_url.rstrip('/')
        self._api_endpoint = api_endpoint.strip('/')

    def _build_url(self, path):
        return f'{self._base_url}/{self._api_endpoint}/{path.lstrip("/")}'

    def _build_request(self, options):
        return self._client.build_request(
            headers=self.default_headers,
            method=options.method,
            url=self._build_url(options.path),
            params=options.params,
        )

    @property
    def default_headers(self):
        return {'User-Agent': 'python-forumlib/1.0.0'}


class SyncAPIClient(BaseClient):
    __slots__ = ('_client',)

    def __init__(self, *, base_url, api_endpoint):
        super().__init__(base_url=base_url, api_endpoint=api_endpoint)
        self._client = httpx.Client()

    def close(self):
        if hasattr(self, '_client'):
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def request(self, options):
        try:
            request = self._build_request(options)
            response = self._client.send(request)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as err:
            print(f'ERROR: request failed: {err}')
        except httpx.HTTPStatusError as err:
            print(f'ERROR: status error: {err.response.status_code}, {err.response.text}')
        except Exception as err:
            print(f'ERROR: unexpected error: {err}')

    def get(self, path, *, params=None):
        return self.request(Options.get(path, params=params))


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


if __name__ == '__main__':
    with ForumLib() as flib:
        print(flib.get_category())
