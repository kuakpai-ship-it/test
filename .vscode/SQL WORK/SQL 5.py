import sqlite3
import os
from datetime import datetime
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "Company.db")

print("="*60)
print("ЗАДАЧА SQL-5: Python + SQL")
print("="*60)

def init_database():
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
    print("✓ База данных готова")

def show_all_employees():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, position, salary, hire_date FROM Employees ORDER BY id")
    rows = cursor.fetchall()
    
    if not rows:
        print("  Нет данных")
        conn.close()
        return []
    
    print("\n" + "="*75)
    print(f"{'ID':<5} {'Имя':<25} {'Должность':<20} {'Зарплата':<12} {'Дата найма':<12}")
    print("="*75)
    
    for row in rows:
        hire_date = row[4] if row[4] else "Не указана"
        print(f"{row[0]:<5} {row[1]:<25} {row[2]:<20} {row[3]:<12.0f} ₸ {hire_date:<12}")
    
    print("="*75)
    print(f"Всего сотрудников: {len(rows)}")
    conn.close()
    return rows

def add_employee():
    print("\n  Введите данные:")
    name = input("  ФИО: ").strip()
    position = input("  Должность: ").strip()
    
    while True:
        try:
            salary = float(input("  Зарплата (тенге): "))
            break
        except ValueError:
            print("  Ошибка! Введите число")
    
    hire_date = input("  Дата найма (ГГГГ-ММ-ДД): ").strip()
    if not hire_date:
        hire_date = datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Employees (name, position, salary, hire_date) 
        VALUES (?, ?, ?, ?)
    """, (name, position, salary, hire_date))
    
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    print(f"\n  ✓ Сотрудник '{name}' добавлен! ID: {new_id}")

def generate_html():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, position, salary, hire_date FROM Employees ORDER BY id")
    employees = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM Employees")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(salary) FROM Employees")
    avg_salary = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT MAX(salary) FROM Employees")
    max_salary = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT MIN(salary) FROM Employees")
    min_salary = cursor.fetchone()[0] or 0
    
    conn.close()
    
    html_path = os.path.join(SCRIPT_DIR, "report_from_sql.html")
    
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отчет о сотрудниках компании</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1300px;
            margin: 0 auto;
        }}
        
        .main-card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .date-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 50px;
            margin-top: 15px;
            font-size: 0.9em;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fc;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .stat-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .stat-card h3 {{
            color: #666;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }}
        
        .stat-value {{
            font-size: 2.2em;
            font-weight: bold;
            color: #333;
        }}
        
        .stat-unit {{
            font-size: 0.8em;
            color: #999;
            margin-left: 5px;
        }}
        
        .stat-sub {{
            color: #888;
            font-size: 0.8em;
            margin-top: 8px;
        }}
        
        .table-wrapper {{
            padding: 0 40px 40px 40px;
        }}
        
        .table-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: inline-block;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.9em;
            letter-spacing: 1px;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
            color: #555;
        }}
        
        tr:hover {{
            background: #f8f9fc;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        .employee-name {{
            font-weight: 600;
            color: #333;
        }}
        
        .salary-high {{
            color: #27ae60;
            font-weight: bold;
        }}
        
        .salary-medium {{
            color: #f39c12;
            font-weight: bold;
        }}
        
        .salary-low {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        .salary-zero {{
            color: #999;
            font-weight: bold;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 500;
        }}
        
        .badge-it {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        
        .badge-hr {{
            background: #fce4ec;
            color: #c2185b;
        }}
        
        .badge-default {{
            background: #f5f5f5;
            color: #666;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
        }}
        
        .footer p {{
            margin: 5px 0;
            opacity: 0.8;
            font-size: 0.9em;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px;
            color: #999;
        }}
        
        .empty-state .icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: 1fr;
            }}
            .table-wrapper {{
                padding: 0 20px 20px 20px;
                overflow-x: auto;
            }}
            .header h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="main-card">
            <div class="header">
                <h1>📊 HR Аналитика</h1>
                <p>Отчет по сотрудникам компании</p>
                <div class="date-badge">
                    📅 Сформирован: {datetime.now().strftime('%d.%m.%Y в %H:%M')}
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-icon">👥</div>
                    <h3>Всего сотрудников</h3>
                    <div class="stat-value">{total}</div>
                    <div class="stat-sub">человек в штате</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">💰</div>
                    <h3>Средняя зарплата</h3>
                    <div class="stat-value">{avg_salary:,.0f}<span class="stat-unit">₸</span></div>
                    <div class="stat-sub">в среднем по компании</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📈</div>
                    <h3>Максимальная</h3>
                    <div class="stat-value">{max_salary:,.0f}<span class="stat-unit">₸</span></div>
                    <div class="stat-sub">самая высокая зарплата</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">📉</div>
                    <h3>Минимальная</h3>
                    <div class="stat-value">{min_salary:,.0f}<span class="stat-unit">₸</span></div>
                    <div class="stat-sub">самая низкая зарплата</div>
                </div>
            </div>
            
            <div class="table-wrapper">
                <div class="table-title">📋 Список сотрудников</div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>ФИО</th>
                            <th>Должность</th>
                            <th>Зарплата</th>
                            <th>Дата найма</th>
                            <th>Статус</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for emp in employees:
        salary = emp[3] or 0
        hire_date = emp[4] if emp[4] else "Не указана"
        
        if salary >= 800000:
            salary_class = "salary-high"
            status = '<span class="badge badge-it">⭐ Ведущий специалист</span>'
        elif salary >= 500000:
            salary_class = "salary-medium"
            status = '<span class="badge badge-it">✅ Сотрудник</span>'
        elif salary > 0:
            salary_class = "salary-low"
            status = '<span class="badge badge-default">📌 Младший специалист</span>'
        else:
            salary_class = "salary-zero"
            status = '<span class="badge badge-default">🎓 Стажер</span>'
        
        html += f"""
                        <tr>
                            <td><strong>{emp[0]}</strong></td>
                            <td class="employee-name">{emp[1]}</td>
                            <td>{emp[2]}</td>
                            <td class="{salary_class}">{salary:,.0f} ₸</td>
                            <td>{hire_date}</td>
                            <td>{status}</td>
                        </tr>"""
    
    if len(employees) == 0:
        html += """
                        <tr>
                            <td colspan="6" class="empty-state">
                                <div class="icon">📭</div>
                                <div>Нет данных о сотрудниках</div>
                                <div style="font-size: 0.9em; margin-top: 10px;">Добавьте первого сотрудника</div>
                            </td>
                        </tr>"""
    
    html += """
                    </tbody>
                </table>
            </div>
            
            <div class="footer">
                <p>🏢 Отчет сгенерирован автоматически из базы данных компании</p>
                <p>© 2026 Все права защищены | Валюта: Казахстанский тенге (₸)</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✓ Отчет создан: report_from_sql.html")
    webbrowser.open(html_path)
    return html_path

def main():
    print("\n[1] Инициализация...")
    init_database()
    
    print("\n[2] Текущие сотрудники:")
    show_all_employees()
    
    print("\n[3] Добавление сотрудника:")
    add_employee()
    
    print("\n[4] Обновленный список:")
    show_all_employees()
    
    print("\n[5] Генерация HTML отчета:")
    generate_html()
    
    print("\n" + "="*60)
    print("✅ Готово! Валюта: Тенге (₸)")
    print("="*60)

if __name__ == "__main__":
    main()