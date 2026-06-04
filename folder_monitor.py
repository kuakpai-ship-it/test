import os
import time
import shutil
from datetime import datetime

# Настройки
INCOMING_FOLDER = "./Incoming"
ARCHIVE_FOLDER = "./Archive"
LOG_FILE = "log.txt"
CHECK_INTERVAL = 10  

# Создаем папки, если их нет
if not os.path.exists(INCOMING_FOLDER):
    os.makedirs(INCOMING_FOLDER)
    print("Создана папка Incoming")

if not os.path.exists(ARCHIVE_FOLDER):
    os.makedirs(ARCHIVE_FOLDER)
    print("Создана папка Archive")

# Создаем файл лога, если его нет
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== Лог мониторинга папки ===\n")
        f.write(f"Запуск: {datetime.now()}\n")
        f.write("=" * 50 + "\n\n")

print("=" * 50)
print("Запуск мониторинга папки Incoming")
print(f"Проверка каждые {CHECK_INTERVAL} секунд")
print("Для остановки нажмите Ctrl+C")
print("=" * 50)

# Список для хранения имен уже обработанных файлов
processed_files = []

# Функция для записи в лог
def write_to_log(new_name, old_name, new_location):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time}] {new_name}\n")
        f.write(f"  Файл: {old_name}\n")
        f.write(f"  Перемещен в: {new_location}\n")
        f.write(f"  {'-' * 40}\n\n")

# Функция для проверки, является ли файл .txt
def that_txt_fail(Filename):
    return Filename.lower().endswith(".txt")

# Функция для создания нового имени с датой
def make_new_name(OldName):
    # Получаем текущее время
    seychas = datetime.now()
    # Форматируем: ГГГГ-ММ-ДД_ЧЧ-ММ-СС
    time_str = seychas.strftime("%Y-%m-%d_%H-%M-%S")
    # Склеиваем: дата_время_оригинальное_имя
    new_name = time_str + "_" + OldName
    return new_name

# Функция для обработки одного файла
def process_the_file(file_path):
    try:
        # Получаем имя файла
        old_name = os.path.basename(file_path)
        
        # Создаем новое имя
        new_name = make_new_name(old_name)
        
        # Полный путь для нового файла в папке Archive
        new_location = os.path.join(ARCHIVE_FOLDER, new_name)
        
        print(f"\nНайден новый файл: {old_name}")
        print(f"Переименовываю в: {new_name}")
        
        # Перемещаем файл (это работает и как переименование, и как перемещение)
        shutil.move(file_path, new_location)
        
        # Записываем в лог
        write_to_log("ПЕРЕМЕЩЕН И ПЕРЕИМЕНОВАН", old_name, new_location)
        
        print(f"Готово! Файл перемещен в Archive")
        return True
        
    except Exception as e:
        print(f"ОШИБКА при обработке файла {old_name}: {e}")
        return False

# Основной цикл программы
try:
    while True:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Проверяю папку Incoming...")
        
        # Получаем список всех файлов в папке Incoming
        try:
            all_files = os.listdir(INCOMING_FOLDER)
        except Exception as e:
            print(f"Не могу прочитать папку: {e}")
            time.sleep(CHECK_INTERVAL)
            continue
        
        # Ищем только .txt файлы
        txt_fail = []
        for fail in all_files:
            if that_txt_fail(fail):
                txt_fail.append(fail)
        
        # Если есть txt файлы
        if len(txt_fail) > 0:
            print(f"Найдено TXT файлов: {len(txt_fail)}")
            
            # Обрабатываем каждый txt файл
            for file_name in txt_fail:
                # Проверяем, не обрабатывали ли мы уже этот файл
                if file_name not in processed_files:
                    # Полный путь к файлу
                    all_path = os.path.join(INCOMING_FOLDER, file_name)
                    
                    # Обрабатываем файл
                    if process_the_file(all_path):
                        # Добавляем в список обработанных
                        processed_files.append(file_name)
                else:
                    print(f"Файл {file_name} уже был обработан, пропускаю")
        else:
            print("Новых TXT файлов не найдено")
        
        # Ждем перед следующей проверкой
        print(f"Жду {CHECK_INTERVAL} секунд...")
        time.sleep(CHECK_INTERVAL)
        
except KeyboardInterrupt:
    print("\n\n" + "=" * 50)
    print("Остановка программы...")
    print(f"Всего обработано файлов: {len(processed_files)}")
    print("Лог сохранен в файле log.txt")
    print("До свидания!")
    print("=" * 50)