from logbook import TimedRotatingFileHandler
import logbook
import os
from ..core.log import RedisSub
from ..core.local import get_current_conf


def path(name):
    return os.path.join(get_current_conf()['TORABOT_DATA_PATH'], name)


def handle(level, bubble=True):
    return TimedRotatingFileHandler(
        path('torabot.%s.log' % level),
        date_format='%Y-%m-%d',
        format_string='[{record.time:%Y-%m-%d %H:%M:%S}] {record.level_name}: {record.channel}: {record.message} {record.extra[context]}',
        level=getattr(logbook, level.upper()),
        bubble=bubble,
    )


def log_to_file():
    sub = RedisSub()
    with logbook.NullHandler().applicationbound():
        with handle('debug'):
            with handle('info'):
                with handle('error'):
                    while sub.dispatch_once(0):
                        pass
