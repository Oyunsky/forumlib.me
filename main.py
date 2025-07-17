import httpx


class Category:
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


class Sort:
    НОВЫЕ = 'newest'
    ПО_ОБНОВЛЕНИЮ = 'updates'
    ОБСУЖДАЕМЫЕ = 'popular'


class Options:
    __slots__ = ('method', 'path', 'params')

    def __init__(self, method, path, *, params=None):
        self.method = method
        self.path = path
        self.params = params

    def __repr__(self):
        repr_fields = ', '.join(f'{s}: {getattr(self, s)!r}' for s in self.__slots__)
        return f'Options({repr_fields})'

    @classmethod
    def get(cls, path, *, params=None):
        return cls('GET', path, params=params)


class BaseClient:
    __slots__ = ('_base_url', '_api_endpoint')

    _client = None

    def __init__(self, base_url, api_endpoint):
        self._base_url = base_url.rstrip('/')
        self._api_endpoint = api_endpoint.strip('/')

    def _build_url(self, path):
        stripped = path.lstrip('/')
        return f'{self._base_url}/{self._api_endpoint}/{stripped}'

    def _build_headers(self):
        return {**self.default_headers}

    def _build_request(self, options):
        return self._client.build_request(
            headers=self._build_headers(),
            method=options.method,
            url=self._build_url(options.path),
            params=options.params,
        )

    @property
    def default_headers(self):
        return {
            'Accept': 'applicatino/json',
            'User-Agent': 'python-forumlib/1.0.0'
        }


class SyncAPIClient(BaseClient):
    __slots__ = ('_client',)

    def __init__(self, base_url, api_endpoint):
        super().__init__(base_url, api_endpoint)

        self._client = httpx.Client()

    def close(self):
        if hasattr(self, '_client'):
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def request(self, options):
        request = self._build_request(options)
        response = self._client.send(request)
        if response.status_code != 200:
            print(f'ERROR: request: failed to send request {response.status_code} {response.reason}')
            return None
        try:
            return response.json()
        except Exception as err:
            print(f'ERROR: request: {err}')
            return None

    def get(self, path, *, params=None):
        options = Options.get(path, params=params)
        return self.request(options)


class ForumLib(SyncAPIClient):
    def __init__(self, base_url=None, api_endpoint=None):
        if not base_url:
            base_url = 'https://forumlib.me'
        if not api_endpoint:
            api_endpoint = '/api/forum'
        super().__init__(base_url, api_endpoint)

    def get_category(self, category=Category.ВСЕ, *, page=1, sort=Sort.НОВЫЕ):
        params = {'category': category, 'page': page, 'sort': sort}
        return self.get('/discussion', params=params)

    def get_discussion(self, discussion_id):
        return self.get(f'/discussion/{discussion_id}')

    def get_comments(self, discussion_id, *, page=1):
        params = {'discussion_id': discussion_id, 'page': page}
        return self.get('/posts', params=params)


def main():
    with ForumLib() as flib:
        xs = flib.get_category()
        print(xs)


if __name__ == '__main__':
    main()
