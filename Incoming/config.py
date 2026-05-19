
from pathlib import Path


BOT_TOKEN = "8795242839:AAFhTmPG_bhU5oZv1rTJsCamPBIFgIh-IlI

# Пути
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
LOG_FILE = BASE_DIR / "bot_log.csv"

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.xlsx', '.xls', '.txt', '.rtf'}

# Максимальный размер файла для отправки (50MB - лимит Telegram)
MAX_FILE_SIZE = 50 * 1024 * 1024

# Настройки поиска
MAX_FILES_IN_RESPONSE = 10
SEARCH_SUBFOLDERS = True