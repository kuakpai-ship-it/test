#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time
from pathlib import Path

def test_rotation():
    """Тестирует создание 7 бэкапов и проверяет что осталось только 5"""
    print("🧪 ЗАПУСК ТЕСТА РОТАЦИИ БЭКАПОВ")
    print("="*60)
    
    # Очищаем старые бэкапы
    backup_dir = Path("./backups")
    if backup_dir.exists():
        for f in backup_dir.glob("backup_*.zip"):
            f.unlink()
        print("✓ Очищены старые бэкапы")
    
    # Создаём 7 бэкапов
    for i in range(1, 8):
        print(f"\n📦 Создание бэкапа #{i}...")
        subprocess.run(["python", "backup_rotate.py"], capture_output=True)
        time.sleep(1)  # Небольшая пауза между бэкапами
    
    # Проверяем результат
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТ ТЕСТА:")
    
    backups = sorted(backup_dir.glob("backup_*.zip"))
    print(f"Создано бэкапов: {len(backups)}")
    
    if len(backups) == 5:
        print("✅ ТЕСТ ПРОЙДЕН! Осталось 5 бэкапов (старые удалены)")
    else:
        print(f"❌ ТЕСТ НЕ ПРОЙДЕН! Ожидалось 5 бэкапов, получено {len(backups)}")
    
    print("\nСписок бэкапов:")
    for i, backup in enumerate(backups, 1):
        print(f"  {i}. {backup.name}")
    
    print("="*60)

if __name__ == "__main__":
    test_rotation()