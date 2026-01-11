$ErrorActionPreference = "Stop"

$python312Url = "https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-amd64.zip"
$destDir = "$env:TEMP\python312_test"
$zipPath = "$destDir\python312.zip"

Write-Host "Creating test directory..."
New-Item -ItemType Directory -Force -Path $destDir | Out-Null

Write-Host "Downloading Python 3.12.8 (embed)..."
Invoke-WebRequest -Uri $python312Url -OutFile $zipPath

Write-Host "Extracting..."
Expand-Archive -Path $zipPath -DestinationPath $destDir -Force

Write-Host "Python 3.12 extracted to: $destDir"
Write-Host "Testing version..."
& "$destDir\python.exe" --version
