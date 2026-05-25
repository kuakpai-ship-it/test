import sqlite3
from datetime import datetime
import os

print("Задача SQL-5: Python + SQL\n")

def show_all():
    """Показать всех сотрудников"""
    conn = sqlite3.connect('Company.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    rows = cursor.fetchall()
    
    print("\n" + "="*65)
    print(f"{'ID':<4} {'Имя':<20} {'Должность':<15} {'Зарплата':<10} {'Дата найма':<12}")
    print("-"*65)
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<20} {row[2]:<15} {row[3]:<10.0f} {row[4]:<12}")
    conn.close()
    return rows

def add_employee():
    """Добавить сотрудника через input"""
    print("\n--- Добавление нового сотрудника ---")
    name = input("Введите имя: ")
    position = input("Введите должность: ")
    salary = float(input("Введите зарплату: "))
    hire_date = input("Дата (ГГГГ-ММ-ДД): ")
    
    conn = sqlite3.connect('Company.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Employees (Name, Position, Salary, HireDate)
    VALUES (?, ?, ?, ?)
    ''', (name, position, salary, hire_date))
    conn.commit()
    conn.close()
    print(f"✓ Сотрудник '{name}' добавлен!")

def generate_html():
    """Создать HTML отчёт"""
    conn = sqlite3.connect('Company.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT e.ID, e.Name, e.Position, e.Salary, e.HireDate, 
               COALESCE(d.DeptName, 'Без отдела')
        FROM Employees e
        LEFT JOIN Departments d ON e.ID = d.EmployeeID
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Отчёт о сотрудниках</title>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Отчёт о сотрудниках</h1>
    <p>Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <table>
        <tr><th>ID</th><th>Имя</th><th>Должность</th><th>Зарплата</th><th>Дата найма</th><th>Отдел</th></tr>
'''
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]:.0f}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"
    
    html += "</table></body></html>"
    
    with open('report_from_sql.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ HTML отчёт создан: {os.path.abspath('report_from_sql.html')}")

# Выполнение всех пунктов
show_all()
add_employee()
print("\nОбновлённый список:")
show_all()
generate_html()
print("\n✅ Задача SQL-5 выполнена!")