# APP INFO
APP_TITLE = 'неТоксичные комментарии'
APP_DESCRIPTION = 'Сервис для выполнения всех операций с комментариями'\
    ', включая ИИ-модерацию'
APP_CONTACT = {
    'Создатель': 'IvanZaycev0717',
    'GitHub': 'https://github.com/IvanZaycev0717/',
    'Telegram': 'https://telegram.me/ivanzaycev0717'
}

# AI MODERATION CONTROL
IS_AI_MODERATION_ENABLED = True
AI_MODERATOR_REQUEST = ('Проанализируй комментарий, и если он токсичный,'
                        'то перепиши его полностью, оставив суть,'
                        'убрав всю токсичность и добавив вежливость,'
                        'а если комментарий не токсичный,'
                        'то верни комментарий'
                        'точь-в-точь таким как он был прислан, без изменений.')

# CORS
BACKEND_URL = 'http://localhost:8000'
FRONTEND_URL = 'http://localhost:5173'

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
