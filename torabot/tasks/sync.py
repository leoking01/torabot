from concurrent.futures import ThreadPoolExecutor as Ex
from ..ut.connection import ccontext
from ..ut.guard import exguard, timeguard
from ..core.sync import sync
from ..db import get_need_sync_queries
from .engine import make as make_engine
from logbook import Logger


log = Logger(__name__)


@timeguard
def sync_all(conf):
    engine = make_engine(conf)

    with ccontext(engine=engine) as conn:
        queries = get_need_sync_queries(conn)

    with Ex(max_workers=conf['TORABOT_SYNC_THREADS']) as ex:
        for query in queries:
            log.debug('sync {} of {}', query.text, query.kind)
            ex.submit(
                exguard(sync),
                kind=query.kind,
                text=query.text,
                engine=engine,
                timeout=conf['TORABOT_SPY_TIMEOUT'],
            )


def sync_one(query_kind, query_text, conf):
    engine = make_engine(conf)
    sync(
        kind=query_kind,
        text=query_text,
        engine=engine,
        timeout=conf['TORABOT_SPY_TIMEOUT'],
    )
