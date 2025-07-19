__all__ = ['Category', 'Sort']

from enum import Enum


class Category(str, Enum):
    ALL = 'all'
    BUGS_AND_ISSUES = '1'
    SITE_SUGGESTIONS = '2'
    TITLE_SEARCH = '3'
    JOB_SEARCH  = '4'
    MANGA_DISCUSSION = '5'
    ANIME_DISCUSSION = '6'
    RANOBE_DISCUSSION = '7'
    VIDEO_GAMES = '8'
    FOR_TRANSLATORS = '9'
    HOW_TO_TRANSLATE_MANGA = '10'
    HOW_TO_DRAW_MANGA = '11'
    GENERAL_CHAT = '12'
    OTHER = '13'


class Sort(str, Enum):
    NEWEST = 'newest'
    UPDATES = 'updates'
    POPULAR = 'popular'