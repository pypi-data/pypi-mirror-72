from contextlib import contextmanager
from logging import getLogger, Logger

from asgiref.sync import sync_to_async
from django.utils.itercompat import is_iterable

try:
    from contextlib import asynccontextmanager
except ImportError:
    from asyncio_extras import async_contextmanager as asynccontextmanager


class AsyncLogWrapper:
    def __init__(self, logger):
        self._logger = logger

    def __getattr__(self, item):
        attr = getattr(self._logger, item)
        if callable(attr):
            attr = sync_to_async(attr, thread_sensitive=True)

        setattr(self, item, attr)
        return attr


# noinspection PyPep8Naming
def getAsyncLogger(name):
    return AsyncLogWrapper(getLogger(name))


@asynccontextmanager
async def async_log_exception(async_logger: AsyncLogWrapper, msg: str, *args, reraise=False, ignore=None):
    # noinspection PyBroadException
    try:
        yield
    except Exception as e:
        if ignore and isinstance(e, tuple(ignore) if is_iterable(ignore) else ignore):
            raise

        await async_logger.exception(msg, *args)
        if reraise:
            raise


@contextmanager
def log_exception(logger: Logger, msg: str, *args, reraise=False, ignore=None):
    # noinspection PyBroadException
    try:
        yield
    except Exception as e:
        if ignore and isinstance(e, tuple(ignore) if is_iterable(ignore) else ignore):
            raise

        logger.exception(msg, *args)
        if reraise:
            raise
