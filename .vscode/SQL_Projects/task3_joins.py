import sqlite3

print("Задача SQL-3: Объединение таблиц (JOIN)\n")

conn = sqlite3.connect('Company.db')
cursor = conn.cursor()

# Создание таблицы Departments
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    DeptID INTEGER PRIMARY KEY AUTOINCREMENT,
    DeptName TEXT NOT NULL,
    EmployeeID INTEGER,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(ID)
)
''')
print("✓ Таблица Departments создана")

# Добавление отделов
departments = [
    ('IT', 1),
    ('IT', 3),
    ('Маркетинг', 5)
]
cursor.executemany('INSERT INTO Departments (DeptName, EmployeeID) VALUES (?, ?)', departments)
conn.commit()
print(f"✓ Добавлено {len(departments)} отделов\n")

# JOIN-запрос
print("SQL-3.3: JOIN-запрос")
cursor.execute('''
SELECT e.Name, e.Position, d.DeptName
FROM Employees e
JOIN Departments d ON e.ID = d.EmployeeID
''')
for row in cursor.fetchall():
    print(f"  • {row[0]} - {row[1]} - Отдел: {row[2]}")

# LEFT JOIN
print("\nSQL-3.4: LEFT JOIN (сотрудники без отдела)")
cursor.execute('''
SELECT e.Name, e.Position
FROM Employees e
LEFT JOIN Departments d ON e.ID = d.EmployeeID
WHERE d.DeptID IS NULL
''')
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"  • {row[0]} - {row[1]} (без отдела)")
else:
    print("  Все сотрудники в отделах")

conn.close()
print("\n✅ Задача SQL-3 выполнена!")