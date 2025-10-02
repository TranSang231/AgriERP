import logging

from django.db import connections

logger = logging.getLogger("project")


class BaseService:
    @staticmethod
    def last_query():
        print('connections: ',connections["default"].queries)

    @classmethod
    def log_exception(cls, exc, full_trace=True):
        logger.error(exc, exc_info=True, stack_info=full_trace)

    @classmethod
    def log_info(cls, message):
        logger.info(message)

    @classmethod
    def log_debug(cls, message):
        logger.debug(message)

    @classmethod
    def log(cls, message):
        logger.error(message)

    class Meta:
        abstract = True
