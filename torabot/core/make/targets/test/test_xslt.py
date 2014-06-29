import os
from ...envs.fs import Env
from ..xslt import Target as XsltTarget


CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))


def read(name):
    with open(os.path.join(CURRENT_PATH, name), 'rb') as f:
        return f.read().decode('utf-8')


def test_request():
    env = Env(root=CURRENT_PATH)
    target = XsltTarget(env)
    assert target(
        html=read('bgm.html'),
        xslt={
            '@type': 'text',
            'name': 'bgm.xslt'
        }
    )