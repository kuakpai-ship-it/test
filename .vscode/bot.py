
import csv
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from telegram import Update, BotCommand, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============= КОНФИГУРАЦИЯ =============
BOT_TOKEN = "8795242839:AAFhTmPG_bhU5oZv1rTJsCamPBIFgIh-IlI"
BASE_DIR = Path(__file__).parent.absolute()
DOCS_DIR = BASE_DIR / "docs"
LOG_FILE = BASE_DIR / "bot_log.csv"

DOCS_DIR.mkdir(exist_ok=True)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def create_all_files():
    """Создание всех тестовых файлов"""
    files_data = [
        ("приказ_№5.txt", "Приказ №5 от 15.01.2025"),
        ("приказ_№15.txt", "Приказ №15 от 20.01.2025"),
        ("приказ_№25.txt", "Приказ №25 от 25.01.2025"),
        ("отчет_2024.txt", "Годовой отчет за 2024 год"),
        ("отчет_январь.txt", "Отчет за январь 2025"),
        ("отчет_февраль.txt", "Отчет за февраль 2025"),
        ("отчет_март.txt", "Отчет за март 2025"),
        ("договор_поставки.txt", "Договор поставки №123"),
        ("договор_аренды.txt", "Договор аренды №456"),
        ("договор_купли.txt", "Договор купли-продажи №789"),
        ("акт_сверки.txt", "Акт сверки за 2024 год"),
        ("акт_выполненных_работ.txt", "Акт выполненных работ №1"),
        ("счет_фактура_45.txt", "Счет-фактура №45"),
        ("счет_фактура_46.txt", "Счет-фактура №46"),
        ("заявление_отпуск.txt", "Заявление на отпуск"),
        ("заявление_увольнение.txt", "Заявление на увольнение"),
        ("справка_доходы.txt", "Справка о доходах"),
        ("справка_налоговая.txt", "Справка 2-НДФЛ"),
        ("инструкция.pdf", "Инструкция пользователя PDF"),
        ("руководство.pdf", "Руководство по эксплуатации PDF"),
        ("приказ_№5.pdf", "Приказ №5 PDF версия"),
        ("приказ_№15.pdf", "Приказ №15 PDF версия"),
        ("отчет_2024.pdf", "Отчет PDF версия"),
        ("отчет_год.pdf", "Годовой отчет PDF"),
        ("договор.docx", "Договор Word версия"),
        ("договор_аренды.docx", "Договор аренды Word"),
        ("финансы.xlsx", "Финансовый отчет Excel"),
        ("бюджет.xlsx", "Бюджет на 2025 год Excel"),
        ("база_клиентов.csv", "Имя,Телефон,Email\nИван,123,ivan@mail.ru\nПетр,456,petr@mail.ru"),
        ("сотрудники.csv", "ФИО,Должность,Оклад\nИванов,Директор,100000\nПетров,Менеджер,50000"),
        ("настройки.json", '{"режим": "рабочий", "версия": "1.0"}'),
        ("config.json", '{"хост": "localhost", "порт": 8080}'),
    ]
    
    for filename, content in files_data:
        file_path = DOCS_DIR / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    files_count = len(list(DOCS_DIR.glob("*")))
    print(f"✅ Создано/проверено файлов: {files_count}")
    return files_count


# Создаём файлы
create_all_files()


def get_all_files() -> List[Path]:
    """Получение ВСЕХ файлов из папки docs"""
    files = []
    if DOCS_DIR.exists():
        for item in DOCS_DIR.iterdir():
            if item.is_file():
                files.append(item)
    return sorted(files)


def search_files(query: str) -> List[Path]:
    """Поиск файлов по полному названию (включая расширение) или по части названия"""
    try:
        all_files = get_all_files()
        found = []
        
        # Очищаем запрос от лишних пробелов
        query = query.strip()
        
        for file_path in all_files:
            # Получаем полное имя файла (с расширением)
            full_name = file_path.name
            # Получаем имя без расширения
            name_without_ext = file_path.stem
            
            # Проверяем три варианта:
            # 1. Точное совпадение с полным именем (без учёта регистра)
            # 2. Частичное совпадение с полным именем
            # 3. Частичное совпадение с именем без расширения
            if (query.lower() == full_name.lower() or
                query.lower() in full_name.lower() or
                query.lower() in name_without_ext.lower()):
                found.append(file_path)
        
        print(f"DEBUG: Поиск '{query}' -> найдено {len(found)} файлов")
        return found
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return []


def log_action(user_id, username, first_name, last_name, command, query, result, file_sent=False):
    """Запись в лог"""
    try:
        file_exists = LOG_FILE.exists()
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists or LOG_FILE.stat().st_size == 0:
                writer.writerow(['timestamp', 'user_id', 'username', 'first_name', 'last_name', 'command', 'query', 'result', 'file_sent'])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, username or "N/A", first_name or "N/A", last_name or "N/A", command, query, result, "Yes" if file_sent else "No"])
    except Exception as e:
        print(f"Ошибка лога: {e}")


async def send_file(update: Update, file_path: Path):
    """Отправка файла"""
    try:
        with open(file_path, 'rb') as f:
            await update.message.reply_document(
                document=InputFile(f, filename=file_path.name),
                caption=f"📄 {file_path.name}"
            )
        return True
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")
        return False


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    files_count = len(get_all_files())
    
    log_action(user.id, user.username, user.first_name, user.last_name, "/start", "", f"справка, файлов: {files_count}", False)
    
    await update.message.reply_text(
        f"🤖 *Бот-ассистент отдела документов*\n\n"
        f"📌 *Команды:*\n"
        f"• /start - показать справку\n"
        f"• /list - показать ВСЕ документы\n"
        f"• /find <текст> - поиск документа\n\n"
        f"📁 *Документов в базе:* {files_count}\n"
        f"🔍 *Примеры поиска:*\n"
        f"• `/find справка_налоговая` - по части имени\n"
        f"• `/find справка_налоговая.txt` - по полному имени\n"
        f"• `/find приказ` - по ключевому слову\n\n"
        f"💡 *Подсказка:* Можно искать как по полному названию файла, так и по части",
        parse_mode="Markdown"
    )


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает ВСЕ файлы без ограничений"""
    user = update.effective_user
    files = get_all_files()
    
    if not files:
        log_action(user.id, user.username, user.first_name, user.last_name, "/list", "", "файлов нет", False)
        await update.message.reply_text(f"❌ Нет файлов в папке {DOCS_DIR}")
        return
    
    log_action(user.id, user.username, user.first_name, user.last_name, "/list", "", f"показано {len(files)} файлов", False)
    
    # Показываем ВСЕ файлы без ограничений
    file_list = []
    for i, file in enumerate(files, 1):
        # Получаем размер файла
        size = file.stat().st_size
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        
        file_list.append(f"{i}. `{file.name}` *({size_str})*")
    
    # Отправляем одним сообщением (если не слишком длинное)
    message = f"📚 *ВСЕ ДОКУМЕНТЫ* (всего: {len(files)})\n\n"
    message += "\n".join(file_list)
    
    # Telegram имеет лимит 4096 символов, если больше - разбиваем на части
    if len(message) > 4000:
        # Отправляем по частям
        for i in range(0, len(file_list), 50):
            part_files = file_list[i:i+50]
            part_message = f"📚 *Документы* ({i+1}-{min(i+50, len(files))} из {len(files)})\n\n"
            part_message += "\n".join(part_files)
            await update.message.reply_text(part_message, parse_mode="Markdown")
    else:
        await update.message.reply_text(message, parse_mode="Markdown")


async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if not context.args:
        await update.message.reply_text(
            "❌ Укажите запрос.\n\n"
            "📝 *Примеры:*\n"
            "• `/find справка_налоговая` - по части имени\n"
            "• `/find справка_налоговая.txt` - по полному имени\n"
            "• `/find приказ` - по ключевому слову",
            parse_mode="Markdown"
        )
        return
    
    query = " ".join(context.args)
    found_files = search_files(query)
    
    if not found_files:
        log_action(user.id, user.username, user.first_name, user.last_name, "/find", query, "ничего не найдено", False)
        
        # Показываем похожие файлы для подсказки
        all_files = get_all_files()
        similar = [f.name for f in all_files if query.lower() in f.name.lower()[:20]]
        
        if similar:
            hint = "\n\n💡 *Возможно, вы искали:*\n" + "\n".join([f"• `{s}`" for s in similar[:5]])
        else:
            hint = "\n\n💡 Используйте `/list` для просмотра всех файлов"
        
        await update.message.reply_text(
            f"🔍 По запросу *{query}* ничего не найдено.{hint}",
            parse_mode="Markdown"
        )
        return
    
    log_action(user.id, user.username, user.first_name, user.last_name, "/find", query, f"найдено {len(found_files)}", False)
    
    if len(found_files) == 1:
        success = await send_file(update, found_files[0])
        if success:
            log_action(user.id, user.username, user.first_name, user.last_name, "/find", query, f"отправлен: {found_files[0].name}", True)
    else:
        # Показываем ВСЕ найденные файлы
        file_list = []
        for i, file in enumerate(found_files, 1):
            file_list.append(f"{i}. `{file.name}`")
        
        message = f"🔍 *Найдено документов:* {len(found_files)}\n\n"
        message += "\n".join(file_list[:30])
        
        if len(found_files) > 30:
            message += f"\n\n... и еще {len(found_files) - 30} файлов"
            await update.message.reply_text(message, parse_mode="Markdown")
        else:
            message += f"\n\n💡 Уточните запрос для получения файла\nПример: `/find {found_files[0].name}`"
            await update.message.reply_text(message, parse_mode="Markdown")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤔 Неизвестная команда. Используйте /start")


async def post_init(application: Application):
    await application.bot.set_my_commands([
        BotCommand("start", "📖 Справка"),
        BotCommand("list", "📋 ВСЕ документы"),
        BotCommand("find", "🔍 Поиск документов"),
    ])
    files_count = len(get_all_files())
    logger.info(f"✅ Бот запущен! Документов: {files_count}")
    print(f"\n{'='*50}")
    print(f"🤖 БОТ ЗАПУЩЕН")
    print(f"📁 Папка: {DOCS_DIR}")
    print(f"📊 Всего файлов: {files_count}")
    print(f"{'='*50}\n")


def main():
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("find", find_command))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    application.run_polling()


if __name__ == "__main__":
    main()