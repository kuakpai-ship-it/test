# schedule_backup.py
import os
import subprocess
from datetime import datetime

print("=== Настройка автоматического бэкапа ===\n")

project_path = r"C:\Users\PREDATOR\OneDrive\Documents\project 1"
script_path = os.path.join(project_path, "backup_db.py")

# Команда для создания задачи
task_name = "Daily_DB_Backup_Project1"
python_path = "python"  # или полный путь: r"C:\Users\PREDATOR\AppData\Local\Programs\Python\Python312\python.exe"

# Создаём задачу в планировщике
cmd = f'''
schtasks /create /tn "{task_name}" /tr "{python_path} {script_path}" /sc daily /st 14:00 /f
'''

print("Для настройки автоматического бэкапа выполните в PowerShell (Администратор):")
print("-" * 60)
print(f'schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc daily /st 14:00 /f')
print("-" * 60)
print("\nИли выполните ручной бэкап: python backup_db.py")