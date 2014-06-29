import jsonpickle
from uuid import uuid4


class Base(object):

    @property
    def name(self):
        key = '_name'
        value = getattr(self, key, None)
        if value is None:
            value = str(uuid4())
            setattr(self, key, value)
        return value

    def __init__(self, env=None):
        self.env = env

    def read(self, name):
        return self.env.read(name)

    def read_text(self, name):
        return self.read(name).decode('utf-8')

    def read_json(self, name):
        return jsonpickle.decode(self.read_text(name))

    def _read(self, name, type):
        return {
            'blob': self.read,
            'text': self.read_text,
            'json': self.read_json,
        }[type](name)

    def preprocess(self, value):
        if isinstance(value, dict) and '@type' in value:
            return self._read(value['name'], value['@type'])
        return value

    @classmethod
    def preprocessed(cls, f):
        def inner(self, *args, **kargs):
            return f(
                self,
                *[self.preprocess(a) for a in args],
                **{key: self.preprocess(kargs[key]) for key in kargs}
            )
        return inner