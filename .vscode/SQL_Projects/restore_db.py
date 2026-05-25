# restore_db.py
import os
import shutil
from datetime import datetime

print(" Восстановление базы данных из бэкапа\n")

project_path = r"C:\Users\PREDATOR\OneDrive\Documents\project 1"
backup_dir = os.path.join(project_path, 'backups')

if not os.path.exists(backup_dir):
    print("❌ Папка с бэкапами не найдена!")
    print("Сначала создайте бэкап через backup_db.py")
    exit(1)

# Получаем список бэкапов
backups = [f for f in os.listdir(backup_dir) if f.startswith('Company_') and f.endswith('.db')]
backups.sort(reverse=True)  # Сортировка от новых к старым

if not backups:
    print("❌ Нет доступных бэкапов!")
    exit(1)

print("📋 Доступные бэкапы:\n")
for i, backup in enumerate(backups, 1):
    backup_path = os.path.join(backup_dir, backup)
    size = round(os.path.getsize(backup_path) / (1024 * 1024), 2)
    # Извлекаем дату из имени файла
    date_part = backup.replace('Company_', '').replace('.db', '')
    print(f"  {i}. {backup}")
    print(f"     Размер: {size} МБ, Дата: {date_part}\n")

# Выбор бэкапа
try:
    choice = int(input("Выберите номер бэкапа для восстановления: "))
    if 1 <= choice <= len(backups):
        selected_backup = backups[choice - 1]
        backup_file = os.path.join(backup_dir, selected_backup)
        
        current_db = os.path.join(project_path, 'Company.db')
        
        # Создаём бэкап текущей БД перед восстановлением
        if os.path.exists(current_db):
            backup_current = os.path.join(
                project_path, 
                f'Company_before_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            )
            shutil.copy2(current_db, backup_current)
            print(f"\n✓ Создан бэкап текущей БД: {backup_current}")
        
        # Восстанавливаем
        shutil.copy2(backup_file, current_db)
        print(f"✓ База данных восстановлена из: {selected_backup}")
        
        # Проверка
        new_size = round(os.path.getsize(current_db) / (1024 * 1024), 2)
        print(f"✓ Размер восстановленной БД: {new_size} МБ")
        
    else:
        print("❌ Неверный номер!")
except ValueError:
    print("❌ Введите число!")