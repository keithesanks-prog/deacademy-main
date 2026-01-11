$version = "3.11.9"
$url = "https://www.python.org/ftp/python/$version/python-$version-embed-amd64.zip"
$output = "python-$version-embed-amd64.zip"
$dest = "python311"

Write-Host "Downloading Python $version..."
Invoke-WebRequest -Uri $url -OutFile $output

Write-Host "Extracting..."
Expand-Archive -Path $output -DestinationPath $dest -Force

# Enable pip (uncomment import site in python311._pth)
$pthInfo = Get-Content "$dest\python311._pth"
$pthInfo | ForEach-Object { 
    if ($_ -match "#import site") { "import site" } else { $_ } 
} | Set-Content "$dest\python311._pth"

# Get pip
Write-Host "Downloading get-pip.py..."
Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"

Write-Host "Installing pip..."
& ".\$dest\python.exe" get-pip.py

Write-Host "Done. Python $version is available in $dest"
& ".\$dest\python.exe" --version
