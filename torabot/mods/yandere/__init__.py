from ...ut.bunch import bunchr
from ..base import Mod
from ..mixins import (
    ViewMixin,
    make_blueprint_mixin
)
from .query import get_query_text


name = 'yandere'


class Yandere(
    ViewMixin,
    make_blueprint_mixin(__name__),
    Mod
):
    name = name
    display_name = 'yande.re'
    has_advanced_search = False
    description = '二次元高清图站, 直接订阅诸如 https://yande.re/post?tags=pantyhose 的链接.'
    normal_search_prompt = '订阅地址/tags'
    allow_empty_query = True

    def view(self, name):
        from .views import web, email
        return {
            'web': web,
            'email': email
        }[name]

    def changes(self, old, new):
        oldmap = {post.id: post for post in getattr(old, 'posts', [])}
        for post in new.posts:
            if post.id not in oldmap:
                yield bunchr(
                    kind='post.new',
                    post=post,
                    query_text=get_query_text(new.query)
                )

    def spy(self, query, timeout):
        from .query import regular
        return super(Yandere, self).spy(regular(query), timeout)
