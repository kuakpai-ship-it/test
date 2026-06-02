# task7_advanced.py
import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "Company.db")

print("="*60)
print("ЗАДАЧА SQL-7: Продвинутые запросы")
print("="*60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ПРОВЕРКА: если таблица пустая, добавляем данные
cursor.execute("SELECT COUNT(*) FROM Employees")
count = cursor.fetchone()[0]

if count == 0:
    print("\nДобавляем тестовые данные...")
    cursor.execute("DELETE FROM Employees")
    cursor.executemany("""
        INSERT INTO Employees (name, position, salary, hire_date) 
        VALUES (?, ?, ?, ?)
    """, [
        ('Иван Петров', 'Разработчик', 75000, '2023-01-15'),
        ('Мария Сидорова', 'Менеджер', 85000, '2022-06-10'),
        ('Алексей Иванов', 'Аналитик', 65000, '2023-03-20'),
        ('Елена Козлова', 'Дизайнер', 70000, '2023-08-01'),
        ('Дмитрий Соколов', 'Тестировщик', 60000, '2024-01-10')
    ])
    conn.commit()
    print(f"Добавлено 5 сотрудников\n")

# ПРОВЕРЯЕМ ЕЩЕ РАЗ
cursor.execute("SELECT COUNT(*) FROM Employees")
count = cursor.fetchone()[0]
print(f"Всего сотрудников: {count}\n")

def print_result(title, rows):
    print(f"\n{title}")
    print("-"*50)
    for row in rows:
        print(" | ".join(str(x) for x in row))
    if rows:
        print(f"\n  Найдено: {len(rows)}")
    else:
        print("  Нет данных")
    print("-"*50)

# ============================================
# SQL-7.1: GROUP BY
# ============================================

print("\n[SQL-7.1] Средняя зарплата по должностям")

cursor.execute("""
    SELECT 
        position,
        COUNT(*) as count,
        ROUND(AVG(salary), 0) as avg_salary,
        MIN(salary) as min_salary,
        MAX(salary) as max_salary
    FROM Employees
    GROUP BY position
    ORDER BY avg_salary DESC
""")

rows = cursor.fetchall()
print_result("Должность | Кол-во | Средняя | Мин | Макс", rows)

# ============================================
# SQL-7.2: Подзапрос
# ============================================

print("\n[SQL-7.2] Сотрудники с зарплатой выше средней")

cursor.execute("""
    SELECT 
        name,
        position,
        salary,
        ROUND((SELECT AVG(salary) FROM Employees), 0) as avg_salary
    FROM Employees
    WHERE salary > (SELECT AVG(salary) FROM Employees)
    ORDER BY salary DESC
""")

rows = cursor.fetchall()
print_result("Имя | Должность | Зарплата | Средняя по компании", rows)

# ============================================
# SQL-7.3: VIEW
# ============================================

print("\n[SQL-7.3] Создание представления")

cursor.execute("DROP VIEW IF EXISTS EmployeeStats")

cursor.execute("""
    CREATE VIEW EmployeeStats AS
    SELECT 
        id,
        name,
        position,
        salary,
        CASE 
            WHEN salary >= 80000 THEN 'Высокая'
            WHEN salary >= 60000 THEN 'Средняя'
            ELSE 'Низкая'
        END as salary_level
    FROM Employees
""")

print("  Представление EmployeeStats создано")

cursor.execute("SELECT * FROM EmployeeStats")
rows = cursor.fetchall()
print_result("ID | Имя | Должность | Зарплата | Уровень", rows)

# ============================================
# SQL-7.4: Функция
# ============================================

print("\n[SQL-7.4] Расчет бонуса")

def calc_bonus(salary):
    return round(salary * 0.15, 0)

conn.create_function("bonus", 1, calc_bonus)

cursor.execute("""
    SELECT 
        name,
        salary,
        bonus(salary) as bonus,
        salary + bonus(salary) as total
    FROM Employees
    ORDER BY total DESC
""")

rows = cursor.fetchall()
print_result("Имя | Зарплата | Бонус 15% | Итого", rows)

# ============================================
# Дополнительные запросы
# ============================================

print("\n" + "="*60)
print("ДОПОЛНИТЕЛЬНЫЕ ЗАПРОСЫ")
print("="*60)

# 1. Топ по зарплате
print("\n[1] Топ сотрудников по зарплате")

cursor.execute("""
    SELECT name, position, salary
    FROM Employees
    ORDER BY salary DESC
    LIMIT 3
""")
rows = cursor.fetchall()
print_result("Имя | Должность | Зарплата", rows)

# 2. Общая статистика
print("\n[2] Общая статистика")

cursor.execute("""
    SELECT 
        COUNT(*) as total,
        ROUND(AVG(salary), 0) as avg_salary,
        MIN(salary) as min_salary,
        MAX(salary) as max_salary,
        SUM(salary) as total_salary
    FROM Employees
""")
rows = cursor.fetchall()
print_result("Всего | Средняя | Мин | Макс | Общая сумма", rows)

# 3. Ранжирование
print("\n[3] Ранжирование сотрудников")

cursor.execute("""
    SELECT 
        name,
        salary,
        RANK() OVER (ORDER BY salary DESC) as rank
    FROM Employees
""")
rows = cursor.fetchall()
print_result("Имя | Зарплата | Место", rows)

# 4. Категории зарплат
print("\n[4] Распределение по категориям")

cursor.execute("""
    SELECT 
        CASE 
            WHEN salary >= 80000 THEN 'Высокая'
            WHEN salary >= 60000 THEN 'Средняя'
            ELSE 'Низкая'
        END as category,
        COUNT(*) as count,
        ROUND(AVG(salary), 0) as avg_salary
    FROM Employees
    GROUP BY category
    ORDER BY avg_salary DESC
""")
rows = cursor.fetchall()
print_result("Категория | Кол-во | Средняя з/п", rows)

# 5. Отклонение от средней
print("\n[5] Отклонение от средней")

cursor.execute("""
    SELECT 
        name,
        salary,
        ROUND(salary - (SELECT AVG(salary) FROM Employees), 0) as diff
    FROM Employees
    ORDER BY diff DESC
""")
rows = cursor.fetchall()
print_result("Имя | Зарплата | Отклонение", rows)

# 6. Количество по должностям
print("\n[6] Количество сотрудников по должностям")

cursor.execute("""
    SELECT 
        position,
        COUNT(*) as count,
        ROUND(AVG(salary), 0) as avg_salary
    FROM Employees
    GROUP BY position
    ORDER BY count DESC
""")
rows = cursor.fetchall()
print_result("Должность | Кол-во | Средняя з/п", rows)

# ============================================
# Итог
# ============================================

print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ")
print("="*60)
print("  SQL-7.1: GROUP BY - выполнено")
print("  SQL-7.2: Подзапрос - выполнен")
print("  SQL-7.3: VIEW - создано")
print("  SQL-7.4: Функция - создана")
print("  Дополнительно: 6 запросов")

conn.close()
print("\nГОТОВО!")