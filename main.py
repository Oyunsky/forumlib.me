from src.forumlib import ForumLib
from src.forumlib.enums import Category


with ForumLib() as flib:
    x = flib.get_category(Category.ОБЩЕНИЕ)
    print(x)