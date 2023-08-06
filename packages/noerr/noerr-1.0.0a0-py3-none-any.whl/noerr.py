# -*- coding: utf-8 -*-
"""
noerr - Catch exceptions with quick context managers

MIT License - Copyright (c) 2020 Chris Griffith - See LICENSE
"""
import logging
import traceback

__all__ = ["NoError", "LogError", "no_err", "log_err"]


class NoError:
    """
    Near equivalent of contextlib.suppress, except it prints the traceback
    """

    def __init__(self, exception_type=Exception):
        self.exception_type = exception_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        catchable = exc_type is not None and issubclass(exc_type, self.exception_type)
        if not catchable:
            if exc_traceback:
                traceback.print_exc()
            return False
        return True


class LogError:
    """
    Log the exception to the indicated logger.

    Can customize log message with {exc_name} or {exc_value}
    """

    def __init__(
        self, exception_type=Exception, log_name=__name__, log_message='{exc_name} logged by "LogError"'
    ):
        self.exception_type = exception_type
        self.log = logging.getLogger(log_name)
        self.log_message = log_message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            self.log.exception(self.log_message.format(exc_name=exc_type.__name__, exc_value=exc_value))
        return exc_type is not None and issubclass(exc_type, self.exception_type)


no_err = NoError()
log_err = LogError()
