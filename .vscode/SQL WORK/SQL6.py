import sqlite3
import os
import shutil
import csv
from datetime import datetime
import json
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "Company.db")
BACKUP_DIR = os.path.join(SCRIPT_DIR, "backups")
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
HISTORY_FILE = os.path.join(SCRIPT_DIR, "db_size_history.csv")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "backup_config.json")

# Создаем необходимые папки
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

print("="*60)
print("ЗАДАЧА SQL-6: Администрирование базы данных")
print("="*60)

# Проверяем и создаем базу данных если её нет
def check_and_create_db():
    """Проверяет наличие БД и создает если нет"""
    if not os.path.exists(DB_PATH):
        print("\n  📁 База данных не найдена. Создаем новую...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL,
                hire_date DATE
            )
        """)
        conn.commit()
        conn.close()
        print("  ✓ База данных создана")
        return True
    return False

def create_backup():
    """Создает резервную копию базы данных"""
    print("\n[SQL-6.1] Создание резервной копии...")
    
    check_and_create_db()
    
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(BACKUP_DIR, f"Company_backup_{date_str}.db")
    
    try:
        shutil.copy2(DB_PATH, backup_file)
        
        size_bytes = os.path.getsize(backup_file)
        size_kb = round(size_bytes / 1024, 2)
        size_mb = round(size_bytes / (1024 * 1024), 2)
        
        write_log({
            "timestamp": datetime.now().isoformat(),
            "action": "backup",
            "status": "success",
            "backup_file": backup_file,
            "size_mb": size_mb
        })
        
        print(f"  ✓ Бэкап создан: Company_backup_{date_str}.db")
        print(f"  ✓ Размер: {size_mb} МБ ({size_kb} КБ)")
        return True
        
    except Exception as e:
        print(f"  ✗ Ошибка: {e}")
        return False

def restore_backup():
    """Восстанавливает базу данных из бэкапа"""
    print("\n[SQL-6.3] Восстановление из бэкапа...")
    
    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith("Company_backup_") and f.endswith(".db")]
    backups.sort(reverse=True)
    
    if not backups:
        print("  ℹ Нет доступных бэкапов. Сначала создайте бэкап (пункт 1)")
        return False
    
    print("\n  Доступные бэкапы:")
    for i, b in enumerate(backups, 1):
        b_path = os.path.join(BACKUP_DIR, b)
        size_mb = round(os.path.getsize(b_path) / (1024 * 1024), 2)
        date_str = b.replace("Company_backup_", "").replace(".db", "")
        print(f"    {i}. {date_str} ({size_mb} МБ)")
    
    try:
        choice = int(input("\n  Выберите номер бэкапа: ")) - 1
        if 0 <= choice < len(backups):
            backup_file = os.path.join(BACKUP_DIR, backups[choice])
            
            # Создаем бэкап текущей БД перед восстановлением
            if os.path.exists(DB_PATH):
                date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                pre_restore_backup = os.path.join(BACKUP_DIR, f"Company_before_restore_{date_str}.db")
                shutil.copy2(DB_PATH, pre_restore_backup)
                print(f"  ✓ Бэкап текущей БД сохранен")
            
            shutil.copy2(backup_file, DB_PATH)
            
            write_log({
                "timestamp": datetime.now().isoformat(),
                "action": "restore",
                "status": "success",
                "restored_from": backups[choice]
            })
            
            print(f"  ✓ База данных восстановлена из бэкапа от {backups[choice].replace('Company_backup_', '').replace('.db', '')}")
            return True
        else:
            print("  ✗ Неверный выбор")
            return False
    except ValueError:
        print("  ✗ Введите число")
        return False

def monitor_size():
    """Отслеживает размер базы данных и записывает в CSV"""
    print("\n[SQL-6.4] Мониторинг размера БД...")
    
    check_and_create_db()
    
    size_bytes = os.path.getsize(DB_PATH)
    size_kb = round(size_bytes / 1024, 2)
    size_mb = round(size_bytes / (1024 * 1024), 2)
    size_gb = round(size_bytes / (1024 * 1024 * 1024), 4)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
    table_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Employees")
    employee_count = cursor.fetchone()[0]
    conn.close()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    file_exists = os.path.exists(HISTORY_FILE)
    
    with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Size_MB", "Size_KB", "Size_Bytes", "Employee_Count", "Table_Count"])
        writer.writerow([timestamp, size_mb, size_kb, size_bytes, employee_count, table_count])
    
    print(f"  📊 Размер БД: {size_mb} МБ ({size_kb} КБ)")
    print(f"  👥 Сотрудников: {employee_count}")
    print(f"  📋 Таблиц: {table_count}")
    print(f"  ✓ История сохранена")
    
    show_size_history()
    return True

def show_size_history():
    """Показывает последние записи истории"""
    if not os.path.exists(HISTORY_FILE):
        return
    
    print("\n  📈 История размера БД:")
    
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        if len(rows) > 1:
            for row in rows[-5:]:
                if len(row) >= 2:
                    print(f"     {row[0]} - {row[1]} МБ ({row[4]} сотрудников)")

def show_all_backups():
    """Показывает все бэкапы"""
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
    backups.sort(reverse=True)
    
    if not backups:
        print("\n  ℹ Нет сохраненных бэкапов")
        return
    
    print("\n  📁 Список бэкапов:")
    total_size = 0
    
    for b in backups:
        b_path = os.path.join(BACKUP_DIR, b)
        size_mb = round(os.path.getsize(b_path) / (1024 * 1024), 2)
        total_size += size_mb
        
        if b.startswith("Company_backup_"):
            type_icon = "💾"
            desc = b.replace("Company_backup_", "").replace(".db", "")
        elif b.startswith("Company_before_restore_"):
            type_icon = "📌"
            desc = b.replace("Company_before_restore_", "").replace(".db", "")
        else:
            type_icon = "📄"
            desc = b
        
        print(f"     {type_icon} {desc} - {size_mb} МБ")
    
    print(f"     📊 Всего: {len(backups)} файлов, {round(total_size, 2)} МБ")

def setup_auto_backup():
    """Настраивает автоматическое резервное копирование"""
    print("\n[SQL-6.2] Настройка автоматического бэкапа...")
    
    config = {
        "auto_backup_enabled": True,
        "backup_time": "02:00",
        "max_backups": 30,
        "last_backup": datetime.now().isoformat()
    }
    
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    print("  ✓ Конфигурация сохранена")
    print("\n  Для настройки автоматического бэкапа в Windows:")
    print("  " + "-"*50)
    print('  1. Откройте Планировщик заданий (taskschd.msc)')
    print('  2. Создайте задачу:')
    print(f'     - Действие: запустить программу "python"')
    print(f'     - Аргументы: "{os.path.join(SCRIPT_DIR, "task6_admin.py")} backup"')
    print('     - Время: ежедневно в 02:00')
    print("  " + "-"*50)

def clean_old_backups():
    """Удаляет старые бэкапы"""
    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith("Company_backup_")]
    backups.sort()
    
    max_backups = 30
    if len(backups) > max_backups:
        to_delete = backups[:-max_backups]
        for b in to_delete:
            os.remove(os.path.join(BACKUP_DIR, b))
        print(f"\n  ✓ Удалено {len(to_delete)} старых бэкапов")
    else:
        print(f"\n  ℹ Всего {len(backups)} бэкапов (лимит {max_backups})")

def generate_size_report():
    """Генерирует HTML отчет по истории размера БД"""
    print("\n  📊 Генерация отчета...")
    
    if not os.path.exists(HISTORY_FILE):
        print("  ℹ Нет данных для отчета. Сначала запустите мониторинг (пункт 3)")
        return
    
    history_data = []
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            history_data.append(row)
    
    if not history_data:
        print("  ℹ Нет данных")
        return
    
    sizes = [float(row["Size_MB"]) for row in history_data]
    
    report_path = os.path.join(SCRIPT_DIR, "db_size_report.html")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>История размера БД</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; background: #f0f2f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; border-radius: 15px; padding: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }}
        h1 {{ color: #667eea; }}
        .stats {{ display: flex; gap: 15px; margin: 20px 0; flex-wrap: wrap; }}
        .card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; flex: 1; text-align: center; }}
        .card .value {{ font-size: 28px; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #667eea; color: white; padding: 12px; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; text-align: center; }}
        tr:hover {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 История размера базы данных</h1>
        <p>Сформирован: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="card"><div class="value">{min(sizes):.2f} МБ</div><div>Минимум</div></div>
            <div class="card"><div class="value">{max(sizes):.2f} МБ</div><div>Максимум</div></div>
            <div class="card"><div class="value">{sum(sizes)/len(sizes):.2f} МБ</div><div>Среднее</div></div>
            <div class="card"><div class="value">{sizes[-1]:.2f} МБ</div><div>Текущий</div></div>
        </div>
        
        <h2>Последние 20 записей</h2>
        <table>
            <thead><tr><th>Дата</th><th>Размер (МБ)</th><th>Сотрудников</th><th>Таблиц</th></tr></thead>
            <tbody>"""
    
    for row in history_data[-20:]:
        html += f"<tr><td>{row['Timestamp']}</td><td>{row['Size_MB']}</td><td>{row['Employee_Count']}</td><td>{row['Table_Count']}</td></tr>"
    
    html += """</tbody>
        </table>
    </div>
</body>
</html>"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✓ Отчет создан: db_size_report.html")
    webbrowser.open(report_path)

def write_log(entry):
    """Записывает событие в лог-файл"""
    log_file = os.path.join(LOG_DIR, f"backup_{datetime.now().strftime('%Y-%m-%d')}.log")
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def main_menu():
    """Интерактивное меню для администрирования"""
    while True:
        print("\n" + "="*60)
        print("SQL-6: Администрирование базы данных")
        print("="*60)
        print("1. 📦 Создать резервную копию (бэкап)")
        print("2. 🔄 Восстановить из бэкапа")
        print("3. 📊 Показать размер БД")
        print("4. 📁 Показать все бэкапы")
        print("5. ⚙ Настроить автоматический бэкап")
        print("6. 📈 Сгенерировать отчет по размеру")
        print("7. 🗑 Очистить старые бэкапы")
        print("0. 🚪 Выход")
        print("="*60)
        
        choice = input("Выберите действие (0-7): ").strip()
        
        if choice == "1":
            create_backup()
        elif choice == "2":
            restore_backup()
        elif choice == "3":
            monitor_size()
        elif choice == "4":
            show_all_backups()
        elif choice == "5":
            setup_auto_backup()
        elif choice == "6":
            generate_size_report()
        elif choice == "7":
            clean_old_backups()
        elif choice == "0":
            print("\n  До свидания!")
            break
        else:
            print("  ✗ Неверный выбор. Введите 0-7")

if __name__ == "__main__":
    import sys
    
    check_and_create_db()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "backup":
            create_backup()
        elif sys.argv[1] == "monitor":
            monitor_size()
        elif sys.argv[1] == "restore":
            restore_backup()
        else:
            main_menu()
    else:
        main_menu()