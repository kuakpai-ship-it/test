# backup_windows.ps1
$env:PGPASSWORD = "1234"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "company_backup_$timestamp.sql"
$zipFile = "company_backup_$timestamp.zip"

Write-Host "Создание бэкапа PostgreSQL..." -ForegroundColor Green
& "C:\Program Files\PostgreSQL\16\bin\pg_dump" -h localhost -p 5432 -U postgres -d Company -f $backupFile --no-owner --no-privileges

if (Test-Path $backupFile) {
    Write-Host "✅ Бэкап создан: $backupFile" -ForegroundColor Green
    Compress-Archive -Path $backupFile -DestinationPath $zipFile -Force
    Remove-Item $backupFile
    Write-Host "✅ Бэкап сжат: $zipFile" -ForegroundColor Green
    
    # Удаляем старые бэкапы (старше 30 дней)
    Get-ChildItem -Filter "company_backup_*.zip" | Where-Object {$_.CreationTime -lt (Get-Date).AddDays(-30)} | Remove-Item
    Write-Host "🗑️ Старые бэкапы удалены" -ForegroundColor Yellow
} else {
    Write-Host "❌ Ошибка создания бэкапа!" -ForegroundColor Red
}
