import sqlite3

print("Задача SQL-7: Продвинутые запросы\n")

conn = sqlite3.connect('Company.db')
cursor = conn.cursor()

# SQL-7.1: GROUP BY и HAVING
print("SQL-7.1: Средняя зарплата по отделам (> 70 000)")
cursor.execute('''
SELECT d.DeptName, AVG(e.Salary) as AvgSalary, COUNT(*) as Count
FROM Employees e
JOIN Departments d ON e.ID = d.EmployeeID
GROUP BY d.DeptName
HAVING AVG(e.Salary) > 70000
''')
for row in cursor.fetchall():
    print(f"  {row[0]}: средняя {row[1]:.0f} тг., сотрудников: {row[2]}")

# SQL-7.2: Подзапрос (выше средней)
print("\nSQL-7.2: Сотрудники с зарплатой выше средней")
cursor.execute('''
SELECT Name, Position, Salary
FROM Employees
WHERE Salary > (SELECT AVG(Salary) FROM Employees)
''')
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}: {row[2]:.0f} тг.")

# SQL-7.3: Создание VIEW
print("\nSQL-7.3: Создание представления")
cursor.execute('DROP VIEW IF EXISTS HighEarners')
cursor.execute('''
CREATE VIEW HighEarners AS
SELECT Name, Position, Salary
FROM Employees
WHERE Salary > 70000
''')
print("✓ Представление 'HighEarners' создано")

# Проверка VIEW
cursor.execute("SELECT * FROM HighEarners")
print("\nСодержимое представления HighEarners:")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}: {row[2]:.0f} тг.")

# SQL-7.4: Функция для расчёта бонуса
def calculate_bonus(salary):
    return salary * 0.15

conn.create_function("bonus", 1, calculate_bonus)
print("\nSQL-7.4: Расчёт бонуса (15% от зарплаты)")
cursor.execute("SELECT Name, Salary, bonus(Salary) FROM Employees")
for row in cursor.fetchall():
    print(f"  {row[0]}: зарплата {row[1]:.0f}, бонус {row[2]:.0f} тг.")

conn.close()
print("\n✅ Задача SQL-7 выполнена!")