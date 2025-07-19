from __future__ import annotations

__all__ = ['BaseClient', 'SyncAPIClient']

from types import TracebackType
from typing import Dict, Type, Generic, TypeVar, Optional

import httpx
from httpx import Request

from ._exceptions import ForumLibException
from ._types import Query, ResponseT, RequestOptions


_T = TypeVar('_T')
_HttpxClientT = TypeVar('_HttpxClientT', bound=httpx.Client)


class BaseClient(Generic[_HttpxClientT]):
    __slots__ = ('_base_url', '_api_endpoint')

    _client: _HttpxClientT
    _base_url: str
    _api_endpoint: str

    def __init__(self, *, base_url: str, api_endpoint: str) -> None:
        self._base_url = base_url.rstrip('/')
        self._api_endpoint = api_endpoint.strip('/')

    def _build_url(self, path: str) -> str:
        return f'{self._base_url}/{self._api_endpoint}/{path.lstrip("/")}'

    def _prepare_params(self, params: Query) -> Query:
        prepped = {}
        for key, value in params.items():
            if key == 'page':
                if not isinstance(value, int):
                    raise TypeError(f'Key `page` must be int, got {type(value).__name__}')
                prepped[key] = max(1, value)
            else:
                prepped[key] = value
        return prepped

    def _build_request(self, options: RequestOptions) -> Request:
        url = self._build_url(options.path)
        prepped_params = self._prepare_params(options.params or {})

        return self._client.build_request(
            headers=self.default_headers,
            method=options.method,
            url=url,
            params=prepped_params
        )

    @property
    def default_headers(self) -> Dict[str, str]:
        return {'User-Agent': 'python-forumlib/1.0.0'}


class SyncAPIClient(BaseClient):
    __slots__ = ('_client',)

    _client: httpx.Client

    def __init__(self, *, base_url: str, api_endpoint: str) -> None:
        super().__init__(base_url=base_url, api_endpoint=api_endpoint)

        self._client = httpx.Client()

    def close(self) -> None:
        if hasattr(self, '_client'):
            self._client.close()

    def __enter__(self: _T) -> _T:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def request(self, options: RequestOptions) -> ResponseT:
        try:
            request = self._build_request(options)
            response = self._client.send(request)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as err:
            raise ForumLibException(f'Network error while sending request: {err}')
        except httpx.HTTPStatusError as err:
            raise ForumLibException(f'Status error: {err.response.status_code}, {err.response.text}')
        except ValueError as err:
            raise ForumLibException(f'Failed to parse JSON from response: {err}')
        except Exception as err:
            raise ForumLibException(f'Unexpected error: {err}')

    def get(self, path: str, *, params: Optional[Query] = None) -> ResponseT:
        return self.request(RequestOptions.get(path, params=params))