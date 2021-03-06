import json
from nose.tools import assert_equal, assert_greater, assert_not_in
from .... import make
from ....core.mod import mod
from ...ut import need_scrapyd
from .. import name
from ..query import parse


@need_scrapyd
def check_spy_contains_query(query):
    app = make()
    with app.test_client():
        d = mod(name).spy(query, 60)
        assert_equal(d.query, parse(query))


def test_spy_contains_query():
    for query in [
        json.dumps(dict(
            method='user_id',
            user_id='511763'
        )),
        json.dumps(dict(
            method='user_uri',
            uri='http://www.pixiv.net/member.php?id=511763'
        )),
        json.dumps(dict(
            method='user_illustrations_uri',
            uri='http://www.pixiv.net/member_illust.php?id=511763'
        )),
        json.dumps(dict(
            method='ranking',
            mode='daily',
            limit=3
        )),
        'http://www.pixiv.net/member.php?id=511763',
        'http://www.pixiv.net/member_illust.php?id=511763',
    ]:
        yield check_spy_contains_query, query


@need_scrapyd
def test_spy_ranking_limit():
    app = make()
    with app.test_client():
        d = mod(name).spy(
            json.dumps(dict(
                method='ranking',
                mode='daily',
                limit=3
            )),
            60
        )
        assert_equal(len(d.arts), 3)


@need_scrapyd
def test_spy_username():
    app = make()
    with app.app_context():
        d = mod(name).spy('北原亜希', 60)
        assert_not_in('recommendations', d)
        assert_greater(len(d.arts), 0)
        assert_greater(d.total, 0)
        d = mod(name).spy('ASK', 60)
        assert_equal(len(d.arts), 0)
        assert_equal(d.total, 0)
        assert_greater(len(d.recommendations), 0)


@need_scrapyd
def check_spy_empty_query(query):
    app = make()
    with app.app_context():
        d = mod(name).spy(query, 60)
        assert_equal(len(d.arts), 0)
        assert_equal(d.total, 0)


def test_spy_empty_query():
    for query in [
        json.dumps(dict(
            method='user_id',
            user_id=''
        )),
        json.dumps(dict(
            method='user_uri',
            uri=''
        )),
        json.dumps(dict(
            method='user_illustrations_uri',
            uri=''
        )),
        json.dumps(dict(
            method='username',
            username=''
        )),
        '',
    ]:
        yield check_spy_empty_query, query
