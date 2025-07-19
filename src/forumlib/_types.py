from __future__ import annotations

__all__ = ['IntOrStr', 'Query', 'ResponseT', 'RequestOptions']

from typing import Any, Dict, List, Type, Union, TypeVar, Mapping, Optional


_T = TypeVar('_T', bound='RequestOptions')

IntOrStr = Union[int, str]
Query = Mapping[str, Optional[Union[str, int, float, bool]]]
ResponseT = Optional[Union[Dict[str, Any], List[Any]]]


class RequestOptions:
    __slots__ = ('method', 'path', 'params')

    def __init__(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Query] = None
    ) -> None:
        self.method = method
        self.path = path
        self.params = params

    @classmethod
    def get(cls: Type[_T], path: str, *, params: Optional[Query] = None) -> _T:
        return cls('GET', path, params=params)