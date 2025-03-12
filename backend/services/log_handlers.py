import logging
from logging.handlers import TimedRotatingFileHandler

from uvicorn.logging import ColourizedFormatter

from settings import LOGGING_FILE_FOLDER, LOGGING_LEVEL

# ДЛЯ ВЫВОДА В КОНСОЛЬ
client_logger = logging.getLogger('client.logger')
client_logger.setLevel(LOGGING_LEVEL)

console_handler = logging.StreamHandler()

console_formatter = ColourizedFormatter(
    "%(levelprefix)s CLIENT CALL - %(message)s",
    use_colors=True,
)
console_handler.setFormatter(console_formatter)
client_logger.addHandler(console_handler)

# ДЛЯ ВЫВОДА В ФАЙЛ
file_handler = TimedRotatingFileHandler(LOGGING_FILE_FOLDER)

file_formatter = logging.Formatter(
    "time %(asctime)s, %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler.setFormatter(file_formatter)
client_logger.addHandler(file_handler)
