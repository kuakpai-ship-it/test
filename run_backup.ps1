# PowerShell скрипт для резервного копирования
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ЗАПУСК РЕЗЕРВНОГО КОПИРОВАНИЯ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\PREDATOR\OneDrive\Documents\project 1"

Write-Host "Текущая папка: C:\Users\PREDATOR\OneDrive\Documents\project 1" -ForegroundColor Yellow
Write-Host ""

Write-Host "Запуск скрипта бэкапа..." -ForegroundColor Green
python backup_rotate.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "РАБОТА ЗАВЕРШЕНА" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Нажмите Enter для выхода"
