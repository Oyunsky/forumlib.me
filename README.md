# Examples

```python
from forumlib import ForumLib
from forumlib.enums import Category

with ForumLib() as flib:
    category = flib.get_category(Category.ALL)
    print(category)

    discussion_id = 593928
    discussion = flib.get_discussion(discussion_id)
    print(discussion)

    comments = flib.get_comments(discussion_id)
    print(comments)
```