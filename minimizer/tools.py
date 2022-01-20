"""
This file is derived from ``tools.py`` of Lab (<https://lab.readthedocs.io>).
Functions and classes that are not needed for this project were removed.
"""
import logging
import os
import sys


DEFAULT_ENCODING = "utf-8"


def get_string(s):
    if isinstance(s, bytes):
        return s.decode(DEFAULT_ENCODING)
    else:
        raise ValueError("tools.get_string() only accepts byte strings")


def get_script_path():
    """Get absolute path to main script."""
    return os.path.abspath(sys.argv[0])


def get_python_executable():
    return sys.executable or "python"


def configure_logging(level=logging.INFO):
    # Python adds a default handler if some log is written before this
    # function is called. We therefore remove all handlers that have
    # been added automatically.
    root_logger = logging.getLogger("")
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)

    class ErrorAbortHandler(logging.StreamHandler):
        """
        Logging handler that exits when a critical error is encountered.
        """

        def emit(self, record):
            logging.StreamHandler.emit(self, record)
            if record.levelno >= logging.CRITICAL:
                sys.exit("aborting")

    class StdoutFilter(logging.Filter):
        def filter(self, record):
            return record.levelno <= logging.WARNING

    class StderrFilter(logging.Filter):
        def filter(self, record):
            return record.levelno > logging.WARNING

    formatter = logging.Formatter("%(asctime)-s %(levelname)-8s %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.addFilter(StdoutFilter())

    stderr_handler = ErrorAbortHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.addFilter(StderrFilter())

    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(stderr_handler)
    root_logger.setLevel(level)


def make_list(value):
    if value is None:
        return []
    elif isinstance(value, list):
        return value[:]
    elif isinstance(value, (tuple, set)):
        return list(value)
    else:
        return [value]


def makedirs(path):
    """
    os.makedirs() variant that doesn't complain if the path already exists.
    """
    try:
        os.makedirs(path)
    except OSError:
        # Directory probably already exists.
        pass

