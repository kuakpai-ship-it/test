import psycopg2
from psycopg2 import sql
import os
import csv
from datetime import datetime
import subprocess

# КОНФИГУРАЦИЯ ПОДКЛЮЧЕНИЯ (ВАШИ ДАННЫЕ)
DB_CONFIG = {
    'dbname': 'Company',      # название базы данных
    'user': 'postgres',       # пользователь
    'password': '1234',       # пароль
    'host': 'localhost',      # сервер
    'port': '5432'            # порт
}

# Путь к утилитам PostgreSQL (измените версию если нужно)
PG_BIN_PATH = r"C:\Program Files\PostgreSQL\16\bin"

def add_pg_to_path():
    if PG_BIN_PATH not in os.environ['PATH']:
        os.environ['PATH'] = PG_BIN_PATH + ";" + os.environ['PATH']

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
def reset_database():
    """Полный сброс базы данных"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Удаляем существующие таблицы
        cursor.execute("DROP TABLE IF EXISTS Departments CASCADE")
        cursor.execute("DROP TABLE IF EXISTS Employees CASCADE")
        
        # Создаём таблицу Employees
        cursor.execute('''
            CREATE TABLE Employees (
                ID SERIAL PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Position VARCHAR(50),
                Salary DECIMAL(10,2),
                HireDate DATE
            )
        ''')
        
        # Создаём таблицу Departments
        cursor.execute('''
            CREATE TABLE Departments (
                DeptID SERIAL PRIMARY KEY,
                DeptName VARCHAR(50),
                EmployeeID INTEGER REFERENCES Employees(ID) ON DELETE CASCADE
            )
        ''')
        
        # Вставляем тестовые данные
        test_data = [
            ("Иванов Иван", "IT", 85000.00, "2023-01-15"),
            ("Петрова Мария", "HR", 65000.00, "2022-11-20"),
            ("Сидоров Алексей", "IT", 95000.00, "2024-03-10"),
            ("Козлова Анна", "Sales", 72000.00, "2023-12-01"),
            ("Михайлов Дмитрий", "Sales", 68000.00, "2023-07-19")
        ]
        
        cursor.executemany(
            "INSERT INTO Employees (Name, Position, Salary, HireDate) VALUES (%s,%s,%s,%s)",
            test_data
        )
        
        # Добавляем отделы
        dept_data = [
            ("IT", 1),
            ("HR", 2),
            ("IT", 3)
        ]
        cursor.executemany(
            "INSERT INTO Departments (DeptName, EmployeeID) VALUES (%s,%s)",
            dept_data
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ База данных сброшена и готова к работе")
        return True
    except Exception as e:
        print(f"❌ Ошибка сброса БД: {e}")
        return False

# ---------- SQL-1: создание БД и таблиц ----------
def sql1_setup():
    print("\n" + "="*60)
    print("SQL-1: Создание базы данных и таблиц")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Создаём таблицу Employees
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                ID SERIAL PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Position VARCHAR(50),
                Salary DECIMAL(10,2),
                HireDate DATE
            )
        ''')
        print("✅ Таблица Employees создана")
        
        # Создаём таблицу Departments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Departments (
                DeptID SERIAL PRIMARY KEY,
                DeptName VARCHAR(50),
                EmployeeID INTEGER REFERENCES Employees(ID) ON DELETE CASCADE
            )
        ''')
        print("✅ Таблица Departments создана")
        
        # Проверяем, есть ли данные
        cursor.execute("SELECT COUNT(*) FROM Employees")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Вставляем тестовые данные
            test_data = [
                ("Иванов Иван", "IT", 85000.00, "2023-01-15"),
                ("Петрова Мария", "HR", 65000.00, "2022-11-20"),
                ("Сидоров Алексей", "IT", 95000.00, "2024-03-10"),
                ("Козлова Анна", "Sales", 72000.00, "2023-12-01"),
                ("Михайлов Дмитрий", "Sales", 68000.00, "2023-07-19")
            ]
            cursor.executemany(
                "INSERT INTO Employees (Name, Position, Salary, HireDate) VALUES (%s,%s,%s,%s)",
                test_data
            )
            print("✅ Добавлено 5 тестовых сотрудников")
            
            # Добавляем отделы
            dept_data = [
                ("IT", 1),
                ("HR", 2),
                ("IT", 3)
            ]
            cursor.executemany(
                "INSERT INTO Departments (DeptName, EmployeeID) VALUES (%s,%s)",
                dept_data
            )
            print("✅ Добавлены отделы")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n📋 Проверка структуры:")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employees")
        for row in cursor.fetchall():
            print(f"  {row}")
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ---------- SQL-2: основные запросы ----------
def sql2_queries():
    print("\n" + "="*60)
    print("SQL-2: Основные запросы")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n📌 SQL-2.1: Зарплата > 70 000")
        cursor.execute("SELECT Name, Position, Salary FROM Employees WHERE Salary > 70000")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"   {row[0]} - {row[1]} - {row[2]:.2f} руб.")
            print(f"   ✅ Результат: {len(rows)} строк")
        else:
            print("   Нет сотрудников")
        
        print("\n📌 SQL-2.2: Устроились после 2023-02-01")
        cursor.execute("SELECT Name, Position, HireDate FROM Employees WHERE HireDate > '2023-02-01'")
        for row in cursor.fetchall():
            print(f"   {row[0]} - {row[1]} - {row[2]}")
        
        print("\n📌 SQL-2.3: Сортировка по зарплате (убывание)")
        cursor.execute("SELECT Name, Position, Salary FROM Employees ORDER BY Salary DESC")
        for row in cursor.fetchall():
            print(f"   {row[0]} - {row[1]} - {row[2]:.2f} руб.")
        
        print("\n📌 SQL-2.4: Средняя зарплата")
        cursor.execute("SELECT AVG(Salary)::DECIMAL(10,2) FROM Employees")
        avg = cursor.fetchone()[0]
        print(f"   Средняя зарплата: {avg:,.2f} руб.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("   Попробуйте сначала выполнить SQL-1")

# ---------- SQL-3: JOIN ----------
def sql3_joins():
    print("\n" + "="*60)
    print("SQL-3: JOIN запросы")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n📌 SQL-3.3: INNER JOIN")
        cursor.execute('''
            SELECT e.Name, e.Position, d.DeptName
            FROM Employees e
            JOIN Departments d ON e.ID = d.EmployeeID
        ''')
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"   {row[0]} - {row[1]} - Отдел: {row[2]}")
            print(f"   ✅ Результат: {len(rows)} строк")
        else:
            print("   Нет данных для JOIN")
        
        print("\n📌 SQL-3.4: LEFT JOIN")
        cursor.execute('''
            SELECT e.Name, e.Position, COALESCE(d.DeptName, 'НЕТ ОТДЕЛА')
            FROM Employees e
            LEFT JOIN Departments d ON e.ID = d.EmployeeID
        ''')
        for row in cursor.fetchall():
            print(f"   {row[0]} - {row[1]} - {row[2]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("   Убедитесь, что таблицы созданы и есть данные")

# ---------- SQL-4: UPDATE / DELETE ----------
def sql4_modifications():
    print("\n" + "="*60)
    print("SQL-4: Изменение данных")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n📌 SQL-4.1: Повышение зарплаты IT на 10%")
        cursor.execute('''
            UPDATE Employees
            SET Salary = Salary * 1.1
            WHERE Position = 'IT'
            RETURNING Name, Salary
        ''')
        updated = cursor.fetchall()
        for name, salary in updated:
            print(f"   ✅ {name} - новая зарплата: {salary:,.2f}")
        
        print("\n📌 SQL-4.2: Удаление сотрудника ID=2")
        cursor.execute("DELETE FROM Employees WHERE ID = 2 RETURNING Name")
        deleted = cursor.fetchone()
        if deleted:
            print(f"   ✅ Удалён: {deleted[0]}")
        
        print("\n📌 SQL-4.3: Оставшиеся сотрудники")
        cursor.execute("SELECT ID, Name, Position, Salary FROM Employees ORDER BY ID")
        for row in cursor.fetchall():
            print(f"   ID:{row[0]} - {row[1]} - {row[2]} - {row[3]:.2f}")
        
        print("\n📌 SQL-4.4: Удаление сотрудников с зарплатой < 70 000")
        cursor.execute("DELETE FROM Employees WHERE Salary < 70000 RETURNING Name, Salary")
        deleted_low = cursor.fetchall()
        for name, salary in deleted_low:
            print(f"   🗑️ Удалён: {name} (зп: {salary:.2f})")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ---------- SQL-5: Python + SQL ----------
def sql5_python_interaction():
    print("\n" + "="*60)
    print("SQL-5: Python + SQL")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n📌 SQL-5.2: Вывод всех сотрудников")
        cursor.execute("SELECT * FROM Employees ORDER BY ID")
        for row in cursor.fetchall():
            print(f"   ID:{row[0]} | {row[1]} | {row[2]} | {row[3]:.2f} | {row[4]}")
        
        print("\n📌 SQL-5.3: Добавление нового сотрудника")
        name = input("   Введите имя: ")
        position = input("   Должность: ")
        salary = float(input("   Зарплата: "))
        hire_date = input("   Дата приёма (ГГГГ-ММ-ДД): ")
        
        cursor.execute(
            "INSERT INTO Employees (Name, Position, Salary, HireDate) VALUES (%s,%s,%s,%s) RETURNING ID",
            (name, position, salary, hire_date)
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        print(f"   ✅ Сотрудник добавлен с ID = {new_id}")
        
        print("\n📌 SQL-5.4: Создание HTML-отчёта")
        cursor.execute("SELECT * FROM Employees ORDER BY ID")
        employees = cursor.fetchall()
        
        html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset='UTF-8'>
            <title>Отчёт из PostgreSQL</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h2 {{ color: #2c3e50; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>📊 Отчёт по сотрудникам компании</h2>
            <p><strong>Дата формирования:</strong> {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</p>
            <p><strong>Всего сотрудников:</strong> {len(employees)}</p>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>ФИО</th>
                        <th>Должность</th>
                        <th>Зарплата (руб.)</th>
                        <th>Дата приёма</th>
                    </tr>
                </thead>
                <tbody>"""
        
        for emp in employees:
            html += f"""
                    <tr>
                        <td>{emp[0]}</td>
                        <td>{emp[1]}</td>
                        <td>{emp[2]}</td>
                        <td style="text-align: right;">{emp[3]:,.2f}</td>
                        <td>{emp[4]}</td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </body>
        </html>"""
        
        with open("report_from_postgres.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("   ✅ HTML-отчёт сохранён: report_from_postgres.html")
        print("   📄 Откройте файл в браузере для просмотра")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ---------- SQL-6: мониторинг и бэкап ----------
def sql6_monitor():
    print("\n" + "="*60)
    print("SQL-6: Мониторинг размера БД")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                pg_database_size(%s) as size_bytes,
                pg_size_pretty(pg_database_size(%s)) as size_pretty
        ''', (DB_CONFIG['dbname'], DB_CONFIG['dbname']))
        
        size_bytes, size_pretty = cursor.fetchone()
        size_mb = size_bytes / (1024 * 1024)
        
        csv_file = "db_size_history.csv"
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Size_MB", "Size_Bytes", "Size_Formatted"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{size_mb:.2f}", size_bytes, size_pretty])
        
        print(f"   📊 Размер БД: {size_pretty} ({size_mb:.2f} MB)")
        print(f"   💾 История сохранена в {csv_file}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def sql6_backup():
    print("\n" + "="*60)
    print("SQL-6: Создание бэкапа")
    print("="*60)
    
    try:
        add_pg_to_path()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"company_backup_{timestamp}.sql"
        
        cmd = [
            'pg_dump',
            '-h', DB_CONFIG['host'],
            '-p', DB_CONFIG['port'],
            '-U', DB_CONFIG['user'],
            '-d', DB_CONFIG['dbname'],
            '-f', backup_file,
            '--no-owner',
            '--no-privileges'
        ]
        
        env = os.environ.copy()
        env['PGPASSWORD'] = DB_CONFIG['password']
        
        print(f"   🔄 Создание бэкапа...")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Бэкап создан: {backup_file}")
            
            # Пробуем сжать
            try:
                zip_file = f"company_backup_{timestamp}.zip"
                subprocess.run(['powershell', '-Command', f'Compress-Archive -Path "{backup_file}" -DestinationPath "{zip_file}" -Force'], 
                             capture_output=True, check=True)
                os.remove(backup_file)
                print(f"   🗜️ Бэкап сжат: {zip_file}")
            except:
                print("   ⚠️ Файл не сжат (можно сжать вручную)")
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ---------- SQL-7: продвинутые запросы ----------
def sql7_advanced():
    print("\n" + "="*60)
    print("SQL-7: Продвинутые запросы")
    print("="*60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n📌 SQL-7.1: GROUP BY + HAVING")
        cursor.execute('''
            SELECT Position, COUNT(*) as cnt, AVG(Salary)::DECIMAL(10,2) as avg_salary
            FROM Employees
            GROUP BY Position
            HAVING AVG(Salary) > 70000
        ''')
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"   {row[0]}: {row[1]} сотрудников, средняя ЗП: {row[2]:,.2f}")
        else:
            print("   Нет должностей со средней зарплатой > 70000")
        
        print("\n📌 SQL-7.2: Подзапрос (сотрудники с зп выше средней)")
        cursor.execute('''
            SELECT Name, Position, Salary
            FROM Employees
            WHERE Salary > (SELECT AVG(Salary) FROM Employees)
            ORDER BY Salary DESC
        ''')
        for row in cursor.fetchall():
            print(f"   {row[0]} - {row[1]} - {row[2]:,.2f}")
        
        print("\n📌 SQL-7.3: Создание VIEW")
        cursor.execute("DROP VIEW IF EXISTS HighEarners")
        cursor.execute('''
            CREATE VIEW HighEarners AS
            SELECT Name, Position, Salary, HireDate
            FROM Employees
            WHERE Salary > 80000
        ''')
        print("   ✅ Представление HighEarners создано")
        
        cursor.execute("SELECT * FROM HighEarners")
        rows = cursor.fetchall()
        if rows:
            print("   Содержимое представления:")
            for row in rows:
                print(f"   {row[0]} - {row[1]} - {row[2]:,.2f} - {row[3]}")
        else:
            print("   Нет сотрудников с зарплатой > 80000")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# ---------- СОЗДАНИЕ POWERSHELL СКРИПТА ДЛЯ БЭКАПА ----------
def create_backup_script():
    ps_script = f'''# backup_windows.ps1
$env:PGPASSWORD = "{DB_CONFIG['password']}"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "company_backup_$timestamp.sql"
$zipFile = "company_backup_$timestamp.zip"

Write-Host "Создание бэкапа PostgreSQL..." -ForegroundColor Green
& "C:\\Program Files\\PostgreSQL\\16\\bin\\pg_dump" -h {DB_CONFIG['host']} -p {DB_CONFIG['port']} -U {DB_CONFIG['user']} -d {DB_CONFIG['dbname']} -f $backupFile --no-owner --no-privileges

if (Test-Path $backupFile) {{
    Write-Host "✅ Бэкап создан: $backupFile" -ForegroundColor Green
    Compress-Archive -Path $backupFile -DestinationPath $zipFile -Force
    Remove-Item $backupFile
    Write-Host "✅ Бэкап сжат: $zipFile" -ForegroundColor Green
    
    # Удаляем старые бэкапы (старше 30 дней)
    Get-ChildItem -Filter "company_backup_*.zip" | Where-Object {{$_.CreationTime -lt (Get-Date).AddDays(-30)}} | Remove-Item
    Write-Host "🗑️ Старые бэкапы удалены" -ForegroundColor Yellow
}} else {{
    Write-Host "❌ Ошибка создания бэкапа!" -ForegroundColor Red
}}
'''
    
    with open("backup_windows.ps1", "w", encoding="utf-8") as f:
        f.write(ps_script)
    
    print("\n📜 Создан PowerShell скрипт: backup_windows.ps1")
    print("   Для автоматического бэкапа выполните (администратор):")
    print("   schtasks /create /tn \"PostgresBackup\" /tr \"powershell -File C:\\путь\\к\\backup_windows.ps1\" /sc daily /st 02:00")

# ---------- ОСНОВНОЕ МЕНЮ ----------
def main():
    print("="*60)
    print("    PostgreSQL + psycopg2 - Решение всех задач")
    print("="*60)
    
    # Проверка подключения
    try:
        test_conn = psycopg2.connect(**DB_CONFIG)
        test_conn.close()
        print(f"✅ Подключение к БД '{DB_CONFIG['dbname']}' успешно!")
        print(f"   Пользователь: {DB_CONFIG['user']}")
        print(f"   Хост: {DB_CONFIG['host']}:{DB_CONFIG['port']}\n")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\nПроверьте:")
        print("1. Запущен ли PostgreSQL (служба)")
        print("2. Правильные логин/пароль")
        print("3. Существует ли база данных 'Company'")
        print("\nСоздайте базу данных в pgAdmin или выполните:")
        print("CREATE DATABASE Company;")
        return
    
    while True:
        print("\n" + "="*60)
        print("Выберите задачу:")
        print("="*60)
        print(" 0. СБРОСИТЬ БД (начать заново с тестовыми данными)")
        print(" 1. SQL-1: Создание таблиц")
        print(" 2. SQL-2: SELECT запросы (WHERE, ORDER BY)")
        print(" 3. SQL-3: JOIN запросы")
        print(" 4. SQL-4: UPDATE и DELETE")
        print(" 5. SQL-5: Python + SQL (input и HTML отчёт)")
        print(" 6. SQL-6: Мониторинг размера БД")
        print(" 7. SQL-6: Создать бэкап")
        print(" 8. SQL-7: Продвинутые запросы (GROUP BY, VIEW)")
        print(" 9. ВЫПОЛНИТЬ ВСЁ (сброс + все задачи)")
        print("10. Создать PowerShell скрипт для бэкапа")
        print("11. Выход")
        
        choice = input("\nВаш выбор: ").strip()
        
        if choice == "0":
            reset_database()
        elif choice == "1":
            sql1_setup()
        elif choice == "2":
            sql2_queries()
        elif choice == "3":
            sql3_joins()
        elif choice == "4":
            sql4_modifications()
        elif choice == "5":
            sql5_python_interaction()
        elif choice == "6":
            sql6_monitor()
        elif choice == "7":
            sql6_backup()
        elif choice == "8":
            sql7_advanced()
        elif choice == "9":
            print("\n🚀 Запуск всех задач...")
            if reset_database():
                sql2_queries()
                sql3_joins()
                sql4_modifications()
                sql5_python_interaction()
                sql7_advanced()
                sql6_monitor()
                sql6_backup()
                print("\n✨ ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")
                print("📁 Созданные файлы:")
                print("   - report_from_postgres.html")
                print("   - db_size_history.csv")
                print("   - company_backup_*.sql или *.zip")
        elif choice == "10":
            create_backup_script()
        elif choice == "11":
            print("До свидания!")
            break
        else:
            print("❌ Неверный выбор!")

if __name__ == "__main__":
    main()