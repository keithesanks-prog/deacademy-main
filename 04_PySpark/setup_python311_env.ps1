$ErrorActionPreference = "Stop"

$workDir = Get-Location
$pythonDir = "$workDir\python311_env"
$pythonVersion = "3.11.9"
$pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-embed-amd64.zip"
$zipPath = "$workDir\python311.zip"
$getPipPath = "$workDir\get-pip.py"

Write-Host "Creating python directory: $pythonDir"
if (Test-Path $pythonDir) {
    Remove-Item -Path $pythonDir -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $pythonDir | Out-Null

if (-not (Test-Path $zipPath)) {
    Write-Host "Downloading Python $pythonVersion..."
    Invoke-WebRequest -Uri $pythonUrl -OutFile $zipPath
}

Write-Host "Extracting Python..."
Expand-Archive -Path $zipPath -DestinationPath $pythonDir -Force

# Enable site-packages for pip
$pthFile = "$pythonDir\python311._pth"
$content = Get-Content $pthFile
$content = $content -replace "#import site", "import site"
Set-Content -Path $pthFile -Value $content
Write-Host "Ensured 'import site' is enabled in _pth file."

if (-not (Test-Path $getPipPath)) {
    Write-Host "Downloading get-pip.py..."
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getPipPath
}

Write-Host "Installing pip..."
& "$pythonDir\python.exe" $getPipPath --no-warn-script-location

Write-Host "Installing PySpark 3.5.3 and Pandas..."
& "$pythonDir\python.exe" -m pip install pyspark==3.5.3 pandas --no-warn-script-location

Write-Host "Setup Complete."
& "$pythonDir\python.exe" --version
& "$pythonDir\python.exe" -m pip show pyspark
