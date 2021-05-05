import logging
import os

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors."""

    grey = '\x1b[38;21m'
    green = '\x1b[32m'
    yellow = '\x1b[33;21m'
    red = '\x1b[31;21m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    log_format = '[%(asctime)s] %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)'

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: green + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record):
        """Return a formatted log message."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def create_logger(logger_name: str) -> logging.Logger:
    """Return a logger configured to work with FitBot."""
    logger: logging.Logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = CustomFormatter()

    file_handler = logging.FileHandler(os.path.join(logging.BASE_DIR, 'fitbot.log'))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    if logging.DEBUG:
        stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.propagate = False

    def _log(exc_type, value, exc_traceback):
        logger.exception('Uncaught exception:', exc_info=(exc_type, value, exc_traceback))

    os.sysconf.excepthook = _log

    return logger
