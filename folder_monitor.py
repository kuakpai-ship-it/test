# folder_monitor.py
# Скрипт для мониторинга папки Incoming
# Новичковый стиль кода - просто и понятно

import os
import time
import shutil
from datetime import datetime

# Настройки
INCOMING_FOLDER = "./Incoming"
ARCHIVE_FOLDER = "./Archive"
LOG_FILE = "log.txt"
CHECK_INTERVAL = 10  # секунд

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
obrabotannye_fayly = []

# Функция для записи в лог
def zapisat_v_log(deystvie, staroe_imya, novoe_mesto):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        vremya = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{vremya}] {deystvie}\n")
        f.write(f"  Файл: {staroe_imya}\n")
        f.write(f"  Перемещен в: {novoe_mesto}\n")
        f.write(f"  {'-' * 40}\n\n")

# Функция для проверки, является ли файл .txt
def eto_txt_fail(imya_faila):
    return imya_faila.lower().endswith(".txt")

# Функция для создания нового имени с датой
def sdelat_novoe_imya(staroe_imya):
    # Получаем текущее время
    seychas = datetime.now()
    # Форматируем: ГГГГ-ММ-ДД_ЧЧ-ММ-СС
    vremya_str = seychas.strftime("%Y-%m-%d_%H-%M-%S")
    # Склеиваем: дата_время_оригинальное_имя
    novoe_imya = vremya_str + "_" + staroe_imya
    return novoe_imya

# Функция для обработки одного файла
def obrabotat_fail(put_k_failu):
    try:
        # Получаем имя файла
        staroe_imya = os.path.basename(put_k_failu)
        
        # Создаем новое имя
        novoe_imya = sdelat_novoe_imya(staroe_imya)
        
        # Полный путь для нового файла в папке Archive
        novyy_put = os.path.join(ARCHIVE_FOLDER, novoe_imya)
        
        print(f"\nНайден новый файл: {staroe_imya}")
        print(f"Переименовываю в: {novoe_imya}")
        
        # Перемещаем файл (это работает и как переименование, и как перемещение)
        shutil.move(put_k_failu, novyy_put)
        
        # Записываем в лог
        zapisat_v_log("ПЕРЕМЕЩЕН И ПЕРЕИМЕНОВАН", staroe_imya, novyy_put)
        
        print(f"Готово! Файл перемещен в Archive")
        return True
        
    except Exception as e:
        print(f"ОШИБКА при обработке файла {staroe_imya}: {e}")
        return False

# Основной цикл программы
try:
    while True:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Проверяю папку Incoming...")
        
        # Получаем список всех файлов в папке Incoming
        try:
            vse_fayly = os.listdir(INCOMING_FOLDER)
        except Exception as e:
            print(f"Не могу прочитать папку: {e}")
            time.sleep(CHECK_INTERVAL)
            continue
        
        # Ищем только .txt файлы
        txt_fayly = []
        for fail in vse_fayly:
            if eto_txt_fail(fail):
                txt_fayly.append(fail)
        
        # Если есть txt файлы
        if len(txt_fayly) > 0:
            print(f"Найдено TXT файлов: {len(txt_fayly)}")
            
            # Обрабатываем каждый txt файл
            for imya_faila in txt_fayly:
                # Проверяем, не обрабатывали ли мы уже этот файл
                if imya_faila not in obrabotannye_fayly:
                    # Полный путь к файлу
                    polnyy_put = os.path.join(INCOMING_FOLDER, imya_faila)
                    
                    # Обрабатываем файл
                    if obrabotat_fail(polnyy_put):
                        # Добавляем в список обработанных
                        obrabotannye_fayly.append(imya_faila)
                else:
                    print(f"Файл {imya_faila} уже был обработан, пропускаю")
        else:
            print("Новых TXT файлов не найдено")
        
        # Ждем перед следующей проверкой
        print(f"Жду {CHECK_INTERVAL} секунд...")
        time.sleep(CHECK_INTERVAL)
        
except KeyboardInterrupt:
    print("\n\n" + "=" * 50)
    print("Остановка программы...")
    print(f"Всего обработано файлов: {len(obrabotannye_fayly)}")
    print("Лог сохранен в файле log.txt")
    print("До свидания!")
    print("=" * 50)