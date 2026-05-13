import sqlite3
from datetime import datetime

def insert_test_data():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()
    
    employees = [
        ('Иванов Иван Иванович', 'Директор', 150000.00, '2020-01-15'),
        ('Петрова Мария Сергеевна', 'Главный бухгалтер', 90000.00, '2021-03-20'),
        ('Сидоров Алексей Владимирович', 'Программист', 80000.00, '2022-06-10'),
        ('Козлова Екатерина Дмитриевна', 'Менеджер по продажам', 75000.00, '2023-01-25'),
        ('Морозов Дмитрий Александрович', 'Аналитик', 85000.00, '2023-09-05')
    ]
    
    cursor.executemany('''
        INSERT INTO Employees (Name, Position, Salary, HireDate)
        VALUES (?, ?, ?, ?)
    ''', employees)
    
    conn.commit()
    
    print(f"Добавлено записей: {len(employees)}")
    
    cursor.execute("SELECT * FROM Employees")
    rows = cursor.fetchall()
    
    print("\nСодержимое таблицы Employees:")
    print("=" * 80)
    print(f"{'ID':<3} {'Name':<25} {'Position':<20} {'Salary':<10} {'HireDate':<12}")
    print("-" * 80)
    
    for row in rows:
        print(f"{row[0]:<3} {row[1]:<25} {row[2]:<20} {row[3]:<10.2f} {row[4]:<12}")
    
    conn.close()

if __name__ == "__main__":
    insert_test_data()