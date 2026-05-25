import sqlite3

print("Задача SQL-4: Изменение данных\n")

conn = sqlite3.connect('Company.db')
cursor = conn.cursor()

# Показываем текущие данные
print("Текущие данные:")
cursor.execute("SELECT ID, Name, Position, Salary FROM Employees")
for row in cursor.fetchall():
    print(f"  ID {row[0]}: {row[1]}, {row[2]}, {row[3]} руб.")

# SQL-4.1: Повышение зарплаты IT
print("\nSQL-4.1: Повышение зарплаты IT на 10%")
cursor.execute('''
UPDATE Employees 
SET Salary = Salary * 1.1
WHERE ID IN (SELECT EmployeeID FROM Departments WHERE DeptName = 'IT')
''')
conn.commit()
print("✓ Зарплата IT повышена")

# SQL-4.2: Удаление сотрудника с ID=2
print("\nSQL-4.2: Удаление сотрудника с ID=2")
cursor.execute("DELETE FROM Employees WHERE ID = 2")
conn.commit()
print("✓ Сотрудник удалён")

# SQL-4.3: Показываем оставшихся
print("\nSQL-4.3: Оставшиеся сотрудники:")
cursor.execute("SELECT ID, Name, Salary FROM Employees")
rows = cursor.fetchall()
for row in rows:
    print(f"  ID {row[0]}: {row[1]}, {row[2]:.0f} руб.")
print(f"  Всего: {len(rows)} сотрудников")

# SQL-4.4: Удаление с зарплатой меньше 70 000
print("\nSQL-4.4: Удаление сотрудников с зарплатой < 70 000")
cursor.execute("DELETE FROM Employees WHERE Salary < 70000")
conn.commit()
print(f"✓ Удалены сотрудники с низкой зарплатой")

# Финальный результат
cursor.execute("SELECT COUNT(*) FROM Employees")
print(f"\nИтоговое количество сотрудников: {cursor.fetchone()[0]}")

conn.close()
print("\n✅ Задача SQL-4 выполнена!")