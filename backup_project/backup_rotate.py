import os
import zipfile
from datetime import datetime
import glob
import shutil

def create_backup():
    """Создание архива папки ./data"""
    # Создаем папку backups если её нет
    os.makedirs('./backups', exist_ok=True)
    
    # Формируем имя файла с текущей датой и временем
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f'backup_{timestamp}.zip'
    backup_path = os.path.join('./backups', backup_name)
    
    # Проверяем существование папки data
    if not os.path.exists('./data'):
        print("Папка ./data не существует. Создаю пустую папку.")
        os.makedirs('./data', exist_ok=True)
    
    # Создаем архив
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('./data'):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, './data')
                zipf.write(file_path, arcname)
    
    print(f"Создан бэкап: {backup_path}")
    return backup_path

def rotate_backups(keep_count=5):
    """Удаляет старые копии, оставляя только последние keep_count штук"""
    # Получаем список всех zip файлов в папке backups
    backup_files = glob.glob('./backups/backup_*.zip')
    
    # Сортируем по времени создания (новые в конце)
    backup_files.sort(key=os.path.getctime)
    
    # Удаляем лишние
    files_to_delete = backup_files[:-keep_count] if len(backup_files) > keep_count else []
    
    for old_file in files_to_delete:
        os.remove(old_file)
        print(f"Удален старый бэкап: {old_file}")
    
    print(f"Текущее количество бэкапов: {min(len(backup_files), keep_count)} из {keep_count}")

def main():
    print(f"=== Запуск бэкапа: {datetime.now()} ===")
    
    # Создаем тестовые файлы в data, если их нет
    if not any(os.scandir('./data')) if os.path.exists('./data') else True:
        os.makedirs('./data', exist_ok=True)
        with open('./data/test.txt', 'w') as f:
            f.write(f"Тестовый файл создан {datetime.now()}")
    
    # Создаем бэкап
    create_backup()
    
    # Выполняем ротацию
    rotate_backups()
    
    print("=== Бэкап завершен ===\n")

if __name__ == "__main__":
    main()