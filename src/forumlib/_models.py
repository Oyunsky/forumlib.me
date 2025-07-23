from __future__ import annotations

__all__ = ['DiscussionModel', 'CategoryModel', 'CommentModel']

import json
from typing import (
    Any,
    Dict,
    List,
    Type,
    Union,
    TypeVar,
    Mapping,
    get_args,
    get_origin,
    get_type_hints,
)

from ._types import AnyMapping


_T = TypeVar('_T', bound='BaseModel')


class BaseModel:
    def __init__(self, **kwargs) -> None:
        self.__fields__: List[str] = []

        for key, value in kwargs.items():
            self.__fields__.append(key)
            setattr(self, key, value)

    def __repr__(self) -> str:
        fields = ', '.join(f'{f}: {getattr(self, f)!r}' for f in self.__fields__)
        return f'{self.__class__.__name__}({fields})'

    def to_dict(self) -> Dict[str, Any]:
        def serialize(value: Any) -> Any:
            if isinstance(value, BaseModel):
                return value.to_dict()
            elif isinstance(value, list):
                return [serialize(item) for item in value]
            elif isinstance(value, dict):
                return {k: serialize(v) for k, v in value.items()}
            else:
                return value
        return {f: serialize(getattr(self, f)) for f in self.__fields__}

    @classmethod
    def parse(cls: Type[_T], data: AnyMapping) -> _T:
        result = {}
        hints = get_type_hints(cls, globals(), locals())
        for f_key, f_type in hints.items():
            f_key = f_key.rstrip('_')
            if f_key not in data:
                result[f_key] = None
                continue

            f_type_origin = get_origin(f_type)
            f_type_args = get_args(f_type)

            if f_type_origin is list:
                item_type = f_type_args[0] if f_type_args else None
                if f_key == 'ops' and isinstance(data, str):
                    data = json.loads(data) # type: ignore
                if item_type and isinstance(item_type, type) and issubclass(item_type, BaseModel):
                    result[f_key] = [item_type.parse(item) for item in data[f_key]]
                elif item_type:
                    result[f_key] = [item_type(item) for item in data[f_key]]
                else:
                    result[f_key] = list(data[f_key])
            elif isinstance(f_type, type) and issubclass(f_type, BaseModel):
                result[f_key] = f_type.parse(data[f_key])
            else:
                result[f_key] = data[f_key]
        return cls(**result)

    @classmethod
    def parse_many(cls: Type[_T], data_list: List[AnyMapping]) -> List[_T]:
        return [cls.parse(item) for item in data_list]


class Attributes(BaseModel):
    italic: bool
    bold: bool
    link: str


class Ops(BaseModel):
    attributes: Attributes
    insert: str


class KeyValue(BaseModel):
    name: str
    version: str


class UserAgent(BaseModel):
    platform: KeyValue
    browser: KeyValue
    device: str
    isDesktop: bool
    isTablet: bool
    isPhone: bool


class Body(BaseModel):
    ops: List[Ops]
    userAgent: UserAgent


class Relation(BaseModel):
    id: int
    cover: str
    slug: str
    value: str
    href: str


class Discussion(BaseModel):
    id: int
    chatter_category_id: int
    title: str
    user_id: int
    source_id: int
    source_type: str
    sticky: int
    locked: int
    views: int
    answered: int
    last_reply_at: str
    created_at: str
    updated_at: str
    deleted_at: str
    yaoi: int
    category_id: int
    category_name: str
    category_slug: str
    category_color: str
    category_icon: str
    username: str
    avatar: str
    notification: bool
    relation: Relation


class Post(BaseModel):
    id: int
    post_id: int
    chatter_category_id: int
    user_id: int
    body: Body
    created_at: str
    updated_at: str
    deleted_at: str


class DiscussionModel(BaseModel):
    discussion: Discussion
    post: Post


class Category(BaseModel):
    id: int
    chatter_category_id: int
    title: str
    user_id: int
    source_id: int
    source_type: str
    sticky: int
    locked: int
    views: int
    answered: int
    last_reply_at: str
    created_at: str
    updated_at: str
    deleted_at: str
    yaoi: int
    category_id: int
    category_name: str
    category_slug: str
    category_color: str
    username: str
    avatar: str
    body: Body


class CategoryModel(BaseModel):
    current_page: int
    data: List[Category]
    first_page_url: str
    from_: int
    next_page_url: str
    path: str
    per_page: int
    prev_page_url: int
    to: int


class Comment(BaseModel):
    id: int
    post_id: int
    chatter_category_id: int
    user_id: int
    body: Body
    created_at: str
    updated_at: str
    deleted_at: str
    username: str
    avatar: str
    reply_username: str
    reply_user_id: int
    user_role: str


class CommentModel(BaseModel):
    current_page: int
    data: List[Comment]
    first_page_url: str
    from_: int
    next_page_url: str
    page: str
    per_page: int
    prev_page_url: str
    to: int