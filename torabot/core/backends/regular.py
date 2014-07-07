from ...ut.bunch import Bunch
from .base import Backend


class Regular(Backend):

    def __init__(self, impl):
        self.impl = impl

    def has_query_bi_kind_and_text(self, kind, text):
        return self.impl.has_query_bi_kind_and_text(kind, text)

    def get_query_bi_kind_and_text(self, kind, text):
        query = self.impl.get_query_bi_kind_and_text(kind, text)
        if query is None:
            return None
        root_kind, root_text = self._get_root_kind_and_text(kind, text)
        root_query = self.impl.get_query_bi_kind_and_text(root_kind, root_text)
        return (
            self._fill_with_root(query, root_query)
            if root_query is not None and query.mtime < root_query.mtime or not query.result
            else query
        )

    def set_next_sync_time_bi_kind_and_text(self, kind, text, time):
        kind, text = self._get_root_kind_and_text(kind, text)
        return self.impl.set_next_sync_time_bi_kind_and_text(kind, text, time)

    def get_or_add_query_bi_kind_and_text(self, kind, text):
        root_kind, root_text = self._get_root_kind_and_text(kind, text)
        self.impl.get_or_add_query_bi_kind_and_text(root_kind, root_text)
        return self.impl.get_or_add_query_bi_kind_and_text(kind, text)

    def touch_query_bi_id(self, id):
        return self.impl.touch_query_bi_id(self._get_root_id(id))

    def add_one_query_changes(self, id, changes):
        return self.impl.add_one_query_changes(id, changes)

    def set_query_result(self, id, result):
        return self.impl.set_query_result(self._get_root_id(id), result)

    def is_query_active_bi_id(self, id):
        return self.impl.is_query_active_bi_id(id)

    def set_next_sync_time(self, id, time):
        return self.impl.set_next_sync_time(self._get_root_id(id), time)

    def get_query_bi_id(self, id):
        query = self.impl.get_query_bi_id(id)
        if query is None:
            return None
        kind, text = self._get_root_kind_and_text(query.kind, query.text)
        if (kind, text) == (query.kind, query.text):
            return query
        root_query = self.impl.get_query_bi_kind_and_text(kind, text)
        return (
            self._fill_with_root(query, root_query)
            if root_query is not None
            else query
        )

    def _get_root_query(self, id):
        query = self.impl.get_query_bi_id(id)
        kind, text = self._get_root_kind_and_text(query.kind, query.text)
        if (kind, text) == (query.kind, query.text):
            return query
        return self.impl.get_query_bi_kind_and_text(kind, text)

    def _get_root_id(self, id):
        return self._get_root_query(id).id

    def _get_root_kind_and_text(self, kind, text):
        from ..query import regular
        return regular(kind, text)

    def _fill_with_root(self, query, root_query):
        return Bunch({key: root_query[key] if key in [
            'result',
            'mtime',
            'next_sync_time',
        ] else query[key] for key in query})
