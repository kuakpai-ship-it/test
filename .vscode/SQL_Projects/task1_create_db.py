import sqlite3

print("Задача SQL-1: Создание базы данных Company\n")

# Создание базы данных
conn = sqlite3.connect('Company.db')
cursor = conn.cursor()
print("✓ База данных Company.db создана")

# Создание таблицы Employees
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Position TEXT NOT NULL,
    Salary REAL NOT NULL,
    HireDate TEXT NOT NULL
)
''')
print("✓ Таблица Employees создана")

# Вставка 5 тестовых записей
employees = [
    ('Иван Петров', 'Разработчик', 75000, '2023-01-15'),
    ('Мария Сидорова', 'Менеджер', 85000, '2022-06-10'),
    ('Алексей Иванов', 'Аналитик', 65000, '2023-03-20'),
    ('Елена Козлова', 'Дизайнер', 70000, '2023-08-01'),
    ('Дмитрий Соколов', 'Тестировщик', 60000, '2024-01-10')
]

cursor.executemany('''
INSERT INTO Employees (Name, Position, Salary, HireDate)
VALUES (?, ?, ?, ?)
''', employees)
conn.commit()
print(f"✓ Добавлено {len(employees)} записей")

# Проверка
cursor.execute("SELECT * FROM Employees")
print("\n--- Содержимое таблицы Employees ---")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Имя: {row[1]}, Должность: {row[2]}, Зарплата: {row[3]} руб., Дата: {row[4]}")

conn.close()
print("\n✅ Задача SQL-1 выполнена!")