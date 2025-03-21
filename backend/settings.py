import logging
import os

# APP INFO
APP_TITLE = 'неТоксичные комментарии'
APP_DESCRIPTION = 'Сервис для выполнения всех операций с комментариями'\
    ', включая ИИ-модерацию'
APP_CONTACT = {
    'Создатель': 'IvanZaycev0717',
    'GitHub': 'https://github.com/IvanZaycev0717/',
    'Telegram': 'https://telegram.me/ivanzaycev0717'
}
# Если хотите запретить доступ к OpenAPI: OPEN_API_ACCESS = None
OPEN_API_ACCESS = '/openapi.json'


# DIRECTORIES AND ENVIROMENTS
BACKEND_ROOT_DIRECTORY = os.getcwd()
ENV_FILENAME = '.env'
ENVIROMENT_FILE = os.path.join(BACKEND_ROOT_DIRECTORY, ENV_FILENAME)


# AI MODERATION CONTROL
IS_AI_MODERATION_ENABLED = False
AI_MODERATOR_REQUEST = ('Проанализируй комментарий, и если он токсичный, '
                        'то перепиши его полностью, оставив суть, '
                        'убрав всю токсичность и добавив вежливость, '
                        'а если комментарий не токсичный, '
                        'то верни комментарий '
                        'точь-в-точь таким как он был прислан, без изменений.')


# CORS
BACKEND_URL = 'http://localhost:8000'
FRONTEND_URL = 'http://localhost:3000'


# DATABASE
SQLAlCHEMY_DATABASE_URI = "sqlite+aiosqlite:///data/database.sql"
SQLALCHEMY_TEST_DATABASE_URI = "sqlite+aiosqlite:///:memory:"


# PROMPT PROPERTIES
# username
MAX_USERNAME_LENGTH = 50
MIN_USERNAME_LENGTH = 2

# comments
MAX_COMMENT_LENGTH = 1000
MIN_COMMENT_LENGTH = 2


# TIMEZONE
TIMEZONE = 'Europe/Moscow'

# LOGGING
LOGGING_LEVEL = logging.INFO
LOGGING_DIRNAME = 'logs'
LOGGING_FILENAME = 'logs.txt'
LOGGING_FILE_FOLDER = os.path.join(
    BACKEND_ROOT_DIRECTORY, LOGGING_DIRNAME, LOGGING_FILENAME
    )
