import sqlite3

print("Задача SQL-2: Основные запросы\n")

conn = sqlite3.connect('Company.db')
cursor = conn.cursor()

# SQL-2.1: Зарплата больше 70 000
print("SQL-2.1: Сотрудники с зарплатой > 70 000")
cursor.execute("SELECT Name, Position, Salary FROM Employees WHERE Salary > 70000")
rows = cursor.fetchall()
for row in rows:
    print(f"  • {row[0]} - {row[1]}: {row[2]} руб.")
print(f"  Результат: {len(rows)} строк(и)\n")

# SQL-2.2: Устроились после 2023-02-01
print("SQL-2.2: Сотрудники, устроившиеся после 2023-02-01")
cursor.execute("SELECT Name, HireDate FROM Employees WHERE HireDate > '2023-02-01'")
rows = cursor.fetchall()
for row in rows:
    print(f"  • {row[0]} - {row[1]}")
print(f"  Результат: {len(rows)} строк(и)\n")

# SQL-2.3: Сортировка по зарплате
print("SQL-2.3: Сотрудники по убыванию зарплаты")
cursor.execute("SELECT Name, Salary FROM Employees ORDER BY Salary DESC")
for i, row in enumerate(cursor.fetchall(), 1):
    print(f"  {i}. {row[0]}: {row[1]} руб.")
print()

# SQL-2.4: Средняя зарплата
cursor.execute("SELECT AVG(Salary) FROM Employees")
avg_salary = cursor.fetchone()[0]
print(f"SQL-2.4: Средняя зарплата: {avg_salary:.2f} руб.")

conn.close()
print("\n✅ Задача SQL-2 выполнена!")