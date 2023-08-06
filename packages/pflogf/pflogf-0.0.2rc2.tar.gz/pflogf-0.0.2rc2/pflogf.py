#!/usr/bin/env python

from colorlog import ColoredFormatter
from shutil import get_terminal_size
import time
import logging
import platform
import sys

# log level color theme from
# https://github.com/FNNDSC/pfmisc/blob/7ecfc7a5b6095761505924fd48e7be3bbd9b1225/pfmisc/debug.py#L144-L149
_COLORS = {
    'DEBUG': 'white',
    'INFO': 'purple',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'fg_red,bg_yellow,bold',
}

_FMT = {
    '%': '%(cyan)s%(asctime)s  |%(hostname)s%(blue)s   %(filename)s | %(log_color)s%(message)s',
    '{': '{cyan}{asctime}  |{hostname}{blue}   {filename} | {log_color}{message}',
    '$': '${cyan}${asctime}  |${hostname}${blue}   ${filename} | ${log_color}${message}'
}

HOSTNAME = platform.node()
_formatted_hostname = f'{HOSTNAME:>15}  |'
_tty_min_columns = 100


class FnndscLogFormatter(ColoredFormatter):
    """
    A colorful log :class:`logging.Formatter` which displays time, hostname, and calling function.
    Its format will be abbreviated if not enough TTY screen output columns are available.
    """

    # it might be better to extract the default style argument from logging
    # inspect.signature(logging.Formatter).parameters['style'].default
    # but for the sake of clarity, '%' is hardcoded below.
    def __init__(self, style='%'):
        """
        :param style: See https://docs.python.org/3/library/logging.html#logging.Formatter
        """
        super().__init__(_FMT[style], reset=True, log_colors=_COLORS, style=style)
        self._wide = True

    def format(self, record):
        self._wide = get_terminal_size((_tty_min_columns, 1)).columns >= _tty_min_columns
        if self._wide:
            record.hostname = _formatted_hostname
            record.filename = f'{record.filename}:{record.funcName}:{record.lineno}'
            record.filename = f'{record.filename:>40}'
        else:
            record.hostname = ''
            record.filename = f'{record.filename}:{record.lineno}'
            record.filename = f'{record.filename:>16}'

        return super().format(record)

    def formatTime(self, record, datefmt=None):
        """
        Produces the current time as a string according to :meth:`logging.Formatter.formatTime`,
        or a shorter HH:MM:SS timestamp if the TTY output screen does not have enough columns available.
        """
        if datefmt:
            return super().formatTime(record, datefmt)
        if self._wide:
            return super().formatTime(record)
        return time.strftime('%H:%M:%S')


def examples():
    """
    Demonstrate the logging output with either some sample messages,
    or strings passed to :data:`sys.argv`.
    """
    if len(sys.argv) > 1:
        data = [' '.join(sys.argv[1:])] * 5
    else:
        data = [
            'debug me as I am full of bugs',
            'an informative statement',
            'you\'ll probably ignore this warning',
            'error, problem exists between keyboard and chair',
            'critical failure, haha jk'
        ]

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(FnndscLogFormatter())
    logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)
    logger.debug(data[0])
    logger.info(data[1])
    logger.warning(data[2])
    logger.error(data[3])
    logger.critical(data[4])


if __name__ == '__main__':
    examples()
