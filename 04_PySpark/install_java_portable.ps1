
$ErrorActionPreference = "Stop"

# Configuration
$javaVersion = "17.0.9+9"
$zipUrl = "https://aka.ms/download-jdk/microsoft-jdk-17.0.9-windows-x64.zip"
$destDir = "$env:USERPROFILE\.gemini\java"
$zipPath = "$destDir\openjdk.zip"

# Create directory
if (!(Test-Path -Path $destDir)) {
    Write-Host "Creating directory: $destDir"
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
}

# Download JDK
Write-Host "Downloading OpenJDK 17 from $zipUrl..."
Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

# Extract JDK
Write-Host "Extracting to $destDir..."
Expand-Archive -Path $zipPath -DestinationPath $destDir -Force

# Find the extracted folder name (it might vary slightly)
$extractedFolder = Get-ChildItem -Path $destDir -Directory | Where-Object { $_.Name -like "jdk-17*" } | Select-Object -First 1

if ($extractedFolder) {
    $javaHome = $extractedFolder.FullName
    Write-Host "✅ Java extracted to: $javaHome"
    
    # Set Environment Variables (User scope)
    Write-Host "Setting JAVA_HOME..."
    [System.Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome, [System.EnvironmentVariableTarget]::User)

    $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
    $binPath = "$javaHome\bin"
    
    if ($currentPath -notlike "*$binPath*") {
        Write-Host "Adding $binPath to Path..."
        $newPath = "$currentPath;$binPath"
        [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::User)
    }
    else {
        Write-Host "Path already contains Java bin."
    }
    
    Write-Host "✅ Installation complete. Please restart your shell/notebook kernel to pick up changes."
}
else {
    Write-Host "❌ Error: Could not find extracted JDK folder."
}

# Cleanup zip
Remove-Item -Path $zipPath -Force
