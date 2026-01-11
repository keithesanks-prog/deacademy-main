
$ErrorActionPreference = "Stop"

$hadoopHome = "$env:USERPROFILE\.hadoop"
$binDir = "$hadoopHome\bin"
$winutilsUrl = "https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.5/bin/winutils.exe"
$hadoopDllUrl = "https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.5/bin/hadoop.dll"

Write-Host "Creating Hadoop directory at $binDir..."
if (!(Test-Path -Path $binDir)) {
    New-Item -ItemType Directory -Force -Path $binDir | Out-Null
}

Write-Host "Downloading winutils.exe..."
Invoke-WebRequest -Uri $winutilsUrl -OutFile "$binDir\winutils.exe"
Write-Host "Downloading hadoop.dll..."
Invoke-WebRequest -Uri $hadoopDllUrl -OutFile "$binDir\hadoop.dll"

Write-Host "Setting Environment Variables..."
[System.Environment]::SetEnvironmentVariable("HADOOP_HOME", $hadoopHome, [System.EnvironmentVariableTarget]::User)

$currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
if ($currentPath -notlike "*$binDir*") {
    $newPath = "$currentPath;$binDir"
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::User)
    Write-Host "Added $binDir to User Path."
}

# Also try to fix /tmp/hive permissions IF we can run winutils
# But we can't easily run it with admin rights to set permissions on C:\tmp\hive usually.
# However, for local spark, it usually tries to use a temp dir.
# If C:\tmp\hive\ permissions are issue, we might need to handle it.
# But just having winutils usually fixes the CheckError.

Write-Host "Installation complete. HADOOP_HOME set to $hadoopHome"
