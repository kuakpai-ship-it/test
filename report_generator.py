#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from collections import defaultdict
from pathlib import Path

def read_csv_file(filename='students.csv'):
    """
    Чтение данных из CSV файла
    
    Args:
        filename (str): имя CSV файла
    
    Returns:
        list: список словарей с данными студентов
    """
    students = []
    
    # Проверяем существование файла
    if not Path(filename).exists():
        print(f"Ошибка: Файл {filename} не найден!")
        print("Создаю пример файла students.csv...")
        create_sample_csv()
        print(f"Файл {filename} создан. Заполните его данными и запустите скрипт снова.")
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Определяем разделитель (запятая или точка с запятой)
            sample = file.read(1024)
            file.seek(0)
            
            if ';' in sample:
                delimiter = ';'
            else:
                delimiter = ','
            
            reader = csv.DictReader(file, delimiter=delimiter)
            
            for row in reader:
                # Приводим ключи к нижнему регистру для удобства
                row = {k.lower(): v for k, v in row.items()}
                
                # Проверяем наличие нужных столбцов
                if 'фио' not in row or 'группа' not in row or 'оценка' not in row:
                    print("Ошибка: CSV файл должен содержать столбцы: ФИО, Группа, Оценка")
                    return None
                
                # Преобразуем оценку в число
                try:
                    grade = float(row['оценка'].replace(',', '.'))
                except ValueError:
                    print(f"Ошибка: Некорректная оценка у студента {row['фио']}")
                    continue
                
                students.append({
                    'name': row['фио'],
                    'group': row['группа'],
                    'grade': grade
                })
    
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None
    
    return students

def create_sample_csv():
    """
    Создание примера CSV файла для демонстрации
    """
    sample_data = [
        ['ФИО', 'Группа', 'Оценка'],
        ['Иванов Иван Иванович', 'Группа А-101', '85'],
        ['Петрова Мария Сергеевна', 'Группа А-101', '92'],
        ['Сидоров Алексей Владимирович', 'Группа А-101', '78'],
        ['Козлова Екатерина Дмитриевна', 'Группа Б-202', '95'],
        ['Морозов Дмитрий Александрович', 'Группа Б-202', '88'],
        ['Волкова Анна Павловна', 'Группа В-303', '91'],
        ['Соколов Артем Игоревич', 'Группа В-303', '84'],
        ['Новикова Ольга Викторовна', 'Группа В-303', '79']
    ]
    
    with open('students.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)
    
    print("Создан пример файла students.csv с тестовыми данными")

def calculate_statistics(students):
    """
    Расчет статистики по группам
    
    Args:
        students (list): список студентов
    
    Returns:
        dict: статистика по группам
    """
    groups_data = defaultdict(lambda: {'grades': [], 'count': 0})
    
    for student in students:
        group = student['group']
        grade = student['grade']
        
        groups_data[group]['grades'].append(grade)
        groups_data[group]['count'] += 1
    
    # Рассчитываем средний балл для каждой группы
    statistics = []
    for group, data in groups_data.items():
        avg_grade = sum(data['grades']) / len(data['grades'])
        statistics.append({
            'group': group,
            'avg_grade': round(avg_grade, 2),
            'student_count': data['count']
        })
    
    # Сортируем по названию группы
    statistics.sort(key=lambda x: x['group'])
    
    return statistics

def generate_html_report(statistics):
    """
    Генерация HTML отчета
    
    Args:
        statistics (list): статистика по группам
    
    Returns:
        str: HTML код отчета
    """
    # Определяем цвет для среднего балла
    def get_grade_color(grade):
        if grade >= 90:
            return '#28a745'  # Зеленый - отлично
        elif grade >= 75:
            return '#17a2b8'  # Голубой - хорошо
        elif grade >= 60:
            return '#ffc107'  # Желтый - удовлетворительно
        else:
            return '#dc3545'  # Красный - плохо
    
    # Генерируем строки таблицы
    table_rows = []
    for group_stat in statistics:
        grade_color = get_grade_color(group_stat['avg_grade'])
        table_rows.append(f"""
            <tr>
                <td><strong>{group_stat['group']}</strong></td>
                <td style="color: {grade_color}; font-weight: bold;">{group_stat['avg_grade']}</td>
                <td>{group_stat['student_count']}</td>
            </tr>
        """)
    
    # Подсчитываем общую статистику
    total_students = sum(stat['student_count'] for stat in statistics)
    overall_avg = sum(stat['avg_grade'] * stat['student_count'] for stat in statistics) / total_students if total_students > 0 else 0
    
    # HTML шаблон
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отчет успеваемости студентов</title>
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
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
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
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .stats-summary {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 40px;
            gap: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            flex: 1;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card h3 {{
            color: #333;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1em;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tbody tr:hover {{
            background-color: #f8f9fa;
            transition: background-color 0.3s ease;
        }}
        
        tbody tr:last-child td {{
            border-bottom: none;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .stats-summary {{
                flex-direction: column;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            th, td {{
                padding: 8px 10px;
                font-size: 0.9em;
            }}
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .badge-excellent {{
            background: #d4edda;
            color: #155724;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Отчет успеваемости студентов</h1>
            <p>Данные успеваемости по группам</p>
        </div>
        
        <div class="content">
            <div class="stats-summary">
                <div class="stat-card">
                    <h3>📚 Всего групп</h3>
                    <div class="value">{len(statistics)}</div>
                </div>
                <div class="stat-card">
                    <h3>👨‍🎓 Всего студентов</h3>
                    <div class="value">{total_students}</div>
                </div>
                <div class="stat-card">
                    <h3>⭐ Общий средний балл</h3>
                    <div class="value">{round(overall_avg, 2)}</div>
                </div>
            </div>
            
            <h2 style="margin-bottom: 20px; color: #333;">Детализация по группам</h2>
            
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>📌 Группа</th>
                            <th>📈 Средний балл</th>
                            <th>👥 Количество студентов</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(table_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>📅 Отчет сгенерирован автоматически | Данные актуальны на момент создания</p>
            <p style="margin-top: 10px; font-size: 0.85em;">Система оценки: 90+ - Отлично | 75-89 - Хорошо | 60-74 - Удовлетворительно | &lt;60 - Требует внимания</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_content

def save_html_report(html_content, filename='report.html'):
    """
    Сохранение HTML отчета в файл
    
    Args:
        html_content (str): HTML код
        filename (str): имя файла для сохранения
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"✅ Отчет успешно создан: {filename}")
        print(f"📂 Полный путь: {Path(filename).absolute()}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")
        return False

def main():
    """
    Основная функция скрипта
    """
    print("=" * 60)
    print("📊 ГЕНЕРАТОР HTML-ОТЧЕТА УСПЕВАЕМОСТИ")
    print("=" * 60)
    
    # Читаем CSV файл
    students = read_csv_file('students.csv')
    
    if students is None:
        print("\n❌ Не удалось загрузить данные. Проверьте файл students.csv")
        return
    
    if len(students) == 0:
        print("❌ Нет данных для обработки")
        return
    
    print(f"✅ Загружено студентов: {len(students)}")
    
    # Рассчитываем статистику
    statistics = calculate_statistics(students)
    print(f"✅ Обработано групп: {len(statistics)}")
    
    # Генерируем HTML отчет
    html_content = generate_html_report(statistics)
    
    # Сохраняем отчет
    if save_html_report(html_content):
        print("\n" + "=" * 60)
        print("🎉 ОТЧЕТ УСПЕШНО СОЗДАН!")
        print("=" * 60)
        print("\n📌 Чтобы открыть отчет в браузере:")
        print("   1. Найдите файл report.html в текущей папке")
        print("   2. Дважды кликните по нему или откройте через браузер")
        print("   3. Либо выполните команду:")
        print("      - Windows: start report.html")
        print("      - Mac: open report.html")
        print("      - Linux: xdg-open report.html")
        print("\n✨ Отчет содержит таблицу с группами, средним баллом и количеством студентов")

if __name__ == "__main__":
    main()