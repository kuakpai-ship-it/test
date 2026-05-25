# backup_db.py
import shutil
import os
from datetime import datetime

print("=== Создание резервной копии базы данных ===\n")

# Путь к вашей папке (автоматически определяется)
project_path = r"C:\Users\PREDATOR\OneDrive\Documents\project 1"
db_file = os.path.join(project_path, 'Company.db')
backup_dir = os.path.join(project_path, 'backups')

# Проверяем существование базы данных
if not os.path.exists(db_file):
    print(f"❌ База данных не найдена: {db_file}")
    print("Сначала выполните task1_create_db.py для создания БД")
    exit(1)

print(f"✓ База данных найдена: {db_file}")

# Создаём папку для бэкапов
os.makedirs(backup_dir, exist_ok=True)
print(f"✓ Папка для бэкапов: {backup_dir}")

# Создаём бэкап с датой
date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = os.path.join(backup_dir, f'Company_{date_str}.db')

shutil.copy2(db_file, backup_file)
print(f"✓ Бэкап создан: {backup_file}")

# Размер файла
size_bytes = os.path.getsize(db_file)
size_kb = round(size_bytes / 1024, 2)
size_mb = round(size_bytes / (1024 * 1024), 2)

print(f"✓ Размер БД: {size_mb} МБ ({size_kb} КБ)")

# История размеров
history_file = os.path.join(project_path, 'db_size_history.csv')
file_exists = os.path.exists(history_file)

with open(history_file, 'a', encoding='utf-8') as f:
    if not file_exists:
        f.write("Дата,Размер_МБ,Размер_КБ,Путь\n")
    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{size_mb},{size_kb},{db_file}\n")

print(f"✓ История сохранена: {history_file}")

# Показываем статистику
print("\n📊 Статистика бэкапов:")
backup_files = [f for f in os.listdir(backup_dir) if f.startswith('Company_')]
print(f"  Всего бэкапов: {len(backup_files)}")
if backup_files:
    print(f"  Последний бэкап: {backup_files[-1]}")

print("\n✅ Бэкап успешно создан!")