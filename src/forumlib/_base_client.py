import httpx

from ._models import Options


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