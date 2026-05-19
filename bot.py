#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram бот для поиска и выдачи документов
Бот-ассистент отдела документооборота
"""

import csv
import re
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from telegram import Update, BotCommand, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ============= КОНФИГУРАЦИЯ =============

BOT_TOKEN = "8795242839:AAFhTmPG_bhU5oZv1rTJsCamPBIFgIh-IlI"

# Пути
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
LOG_FILE = BASE_DIR / "bot_log.csv"

# Разрешенные расширения
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.xlsx', '.xls', '.txt', '.rtf'}

# Максимальный размер файла (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

# Создаем папку для документов
DOCS_DIR.mkdir(exist_ok=True)

# ============= НАСТРОЙКА ЛОГИРОВАНИЯ =============

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# ============= ОСНОВНОЙ КЛАСС БОТА =============

class DocsBot:
    """Класс для работы с ботом документов"""
    
    def __init__(self):
        """Инициализация бота"""
        self.docs_dir = DOCS_DIR
        self.log_file = LOG_FILE
        self.init_log_file()
        
    def init_log_file(self):
        """Инициализация CSV лог-файла"""
        if not self.log_file.exists():
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'user_id', 'username', 
                    'first_name', 'last_name', 'command', 
                    'query', 'result', 'file_sent'
                ])
            logger.info(f"Создан файл лога: {self.log_file}")
    
    def log_action(self, user_id: int, username: str, first_name: str, 
                   last_name: str, command: str, query: str, 
                   result: str, file_sent: bool = False):
        """Запись действия в лог"""
        try:
            with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_id,
                    username or "N/A",
                    first_name or "N/A",
                    last_name or "N/A",
                    command,
                    query,
                    result,
                    "Yes" if file_sent else "No"
                ])
            logger.info(f"Лог записан: {user_id} - {command} - {query}")
        except Exception as e:
            logger.error(f"Ошибка записи лога: {e}")
    
    def get_all_files(self) -> List[Path]:
        """Получение списка всех файлов в директории docs"""
        files = []
        if not self.docs_dir.exists():
            return files
        
        for ext in ALLOWED_EXTENSIONS:
            files.extend(self.docs_dir.glob(f"*{ext}"))
            files.extend(self.docs_dir.glob(f"*{ext.upper()}"))
        
        files.sort(key=lambda x: x.name)
        return files
    
    def search_files(self, pattern: str) -> List[Path]:
        """Поиск файлов по регулярному выражению"""
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            all_files = self.get_all_files()
            found = [f for f in all_files if regex.search(f.stem)]
            logger.info(f"Поиск '{pattern}': найдено {len(found)} файлов")
            return found
        except re.error as e:
            logger.error(f"Ошибка регулярного выражения: {e}")
            return []
    
    def get_file_info(self, file_path: Path) -> Dict:
        """Получение информации о файле"""
        if not file_path.exists():
            return None
        
        stat = file_path.stat()
        size_mb = stat.st_size / (1024 * 1024)
        
        return {
            'name': file_path.name,
            'size_mb': round(size_mb, 2),
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            'path': file_path
        }
    
    async def send_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                        file_path: Path) -> bool:
        """Отправка файла пользователю"""
        try:
            file_size = file_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                await update.message.reply_text(
                    f"❌ Файл слишком большой ({file_size / (1024*1024):.1f}MB). "
                    f"Максимальный размер: 50MB"
                )
                return False
            
            with open(file_path, 'rb') as f:
                await update.message.reply_document(
                    document=InputFile(f, filename=file_path.name),
                    caption=f"📄 Документ: {file_path.name}\n"
                            f"📏 Размер: {file_size / (1024*1024):.2f} MB"
                )
            
            logger.info(f"Файл отправлен: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки файла: {e}")
            await update.message.reply_text(f"❌ Ошибка при отправке файла: {str(e)}")
            return False


# Инициализация бота
docs_bot = DocsBot()


# ============= ОБРАБОТЧИКИ КОМАНД =============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start - показывает справку"""
    user = update.effective_user
    
    docs_bot.log_action(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        command="/start",
        query="",
        result="справка показана"
    )
    
    files_count = len(docs_bot.get_all_files())
    
    help_text = f"""
🤖 *Бот-ассистент отдела документооборота*

Привет! Я помогу найти и получить документы из нашей базы.

📌 *Доступные команды:*

• `/start` - Показать эту справку
• `/list` - Показать список всех доступных документов
• `/find <запрос>` - Поиск документов по названию

🔍 *Примеры поиска:*
• `/find отчет` - найдет все файлы со словом "отчет"
• `/find приказ` - найдет все приказы
• `/find 2024` - найдет файлы с 2024 в названии

📁 *Поддерживаемые форматы:*
PDF, DOCX, DOC, XLSX, XLS, TXT, RTF

📊 *Статистика:*
Всего документов в базе: {files_count}

Для поиска просто напишите `/find` и ключевое слово!

© Отдел документационного обеспечения
    """
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /list - показывает список всех документов"""
    user = update.effective_user
    
    files = docs_bot.get_all_files()
    
    if not files:
        docs_bot.log_action(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            command="/list",
            query="",
            result="документов не найдено"
        )
        
        await update.message.reply_text(
            "📭 В базе документов пока нет файлов.\n\n"
            "Пожалуйста, добавьте документы в папку ./docs/"
        )
        return
    
    docs_bot.log_action(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        command="/list",
        query="",
        result=f"показано {len(files)} документов"
    )
    
    doc_list = []
    for i, file in enumerate(files[:50], 1):
        info = docs_bot.get_file_info(file)
        doc_list.append(f"{i}. 📄 *{file.name}* ({info['size_mb']} MB)")
    
    message = f"📚 *Доступные документы:*\nВсего: {len(files)}\n\n"
    message += "\n".join(doc_list)
    
    if len(files) > 50:
        message += f"\n\n... и еще {len(files) - 50} документов"
    
    message += "\n\n🔍 Используйте `/find <запрос>` для поиска"
    
    await update.message.reply_text(message, parse_mode="Markdown")


async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /find - поиск документов"""
    user = update.effective_user
    
    if not context.args:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите поисковый запрос.\n"
            "Пример: `/find отчет`", 
            parse_mode="Markdown"
        )
        return
    
    query = " ".join(context.args)
    found_files = docs_bot.search_files(query)
    
    if not found_files:
        docs_bot.log_action(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            command="/find",
            query=query,
            result="ничего не найдено",
            file_sent=False
        )
        
        await update.message.reply_text(
            f"🔍 По запросу *{query}* ничего не найдено.\n\n"
            f"Попробуйте:\n"
            f"• Использовать другое ключевое слово\n"
            f"• Посмотреть все документы через /list\n"
            f"• Проверить правильность написания",
            parse_mode="Markdown"
        )
        return
    
    docs_bot.log_action(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        command="/find",
        query=query,
        result=f"найдено {len(found_files)} файлов",
        file_sent=False
    )
    
    # Если найден один файл - отправляем
    if len(found_files) == 1:
        success = await docs_bot.send_file(update, context, found_files[0])
        
        if success:
            docs_bot.log_action(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                command="/find",
                query=query,
                result=f"отправлен файл: {found_files[0].name}",
                file_sent=True
            )
    else:
        # Несколько файлов - показываем список
        files_list = []
        for i, file in enumerate(found_files[:10], 1):
            info = docs_bot.get_file_info(file)
            files_list.append(f"{i}. {file.name} ({info['size_mb']} MB)")
        
        message = f"🔍 *Найдено документов:* {len(found_files)}\n\n"
        
        if len(found_files) > 10:
            message += f"*Первые 10 из {len(found_files)}:*\n\n"
        else:
            message += "*Документы:*\n\n"
        
        message += "\n".join(files_list)
        message += "\n\n💡 *Совет:* Уточните запрос, чтобы получить конкретный документ"
        
        await update.message.reply_text(message, parse_mode="Markdown")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик неизвестных команд"""
    await update.message.reply_text(
        "🤔 Неизвестная команда.\n"
        "Используйте /start для просмотра доступных команд."
    )


async def post_init(application: Application):
    """Настройка команд бота после инициализации"""
    await application.bot.set_my_commands([
        BotCommand("start", "📖 Показать справку"),
        BotCommand("list", "📋 Список всех документов"),
        BotCommand("find", "🔍 Поиск документов (например: /find отчет)"),
    ])
    
    logger.info("Бот успешно запущен!")
    files_count = len(docs_bot.get_all_files())
    logger.info(f"Документов в базе: {files_count}")
    logger.info(f"Папка документов: {DOCS_DIR.absolute()}")
    logger.info(f"Лог-файл: {LOG_FILE.absolute()}")


# ============= ЗАПУСК БОТА =============

def main():
    """Главная функция запуска бота"""
    
    # Создание папки для документов
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir(parents=True)
        print(f"\n📁 Создана папка для документов: {DOCS_DIR.absolute()}")
    
    # Создание примера документа
    if len(docs_bot.get_all_files()) == 0:
        example_file = DOCS_DIR / "пример_документа_отчет.txt"
        with open(example_file, 'w', encoding='utf-8') as f:
            f.write("Пример документа для тестирования бота.\n")
            f.write("Поместите сюда ваши реальные документы.\n")
            f.write("Поддерживаются форматы: PDF, DOCX, XLSX, TXT и другие.\n")
        print(f"📄 Создан пример документа: {example_file.name}")
        print("   Замените его на свои документы!\n")
    
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("find", find_command))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Запуск
    print("\n" + "="*60)
    print("🤖 БОТ-АССИСТЕНТ ЗАПУЩЕН")
    print("="*60)
    print(f"📁 Папка с документами: {DOCS_DIR.absolute()}")
    print(f"📄 Лог-файл: {LOG_FILE.absolute()}")
    print(f"📊 Документов в базе: {len(docs_bot.get_all_files())}")
    print("="*60)
    print("\n✅ Бот готов к работе! Нажмите Ctrl+C для остановки\n")
    
    # Запуск бота
    application.run_polling()


if __name__ == "__main__":
    main()