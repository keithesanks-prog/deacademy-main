# PowerShell script to patch pyspark.zip for Windows compatibility

$ErrorActionPreference = "Stop"

$zipPath = "C:\Users\ksank\training\.venv312\Lib\site-packages\pyspark\python\lib\pyspark.zip"
$extractPath = "C:\Users\ksank\training\.venv312\Lib\site-packages\pyspark\python\lib\pyspark_extracted"
$backupPath = "C:\Users\ksank\training\.venv312\Lib\site-packages\pyspark\python\lib\pyspark.zip.backup"

Write-Host "Step 1: Creating backup of pyspark.zip..."
if (!(Test-Path $backupPath)) {
    Copy-Item $zipPath $backupPath
    Write-Host "  Backup created: $backupPath"
}
else {
    Write-Host "  Backup already exists"
}

Write-Host "`nStep 2: Extracting pyspark.zip..."
if (Test-Path $extractPath) {
    Remove-Item $extractPath -Recurse -Force
}
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
Write-Host "  Extracted to: $extractPath"

Write-Host "`nStep 3: Patching accumulators.py..."
$accumulatorsPath = Join-Path $extractPath "pyspark\accumulators.py"

if (!(Test-Path $accumulatorsPath)) {
    Write-Host "  ERROR: accumulators.py not found at $accumulatorsPath"
    exit 1
}

# Read the file
$content = Get-Content $accumulatorsPath -Raw

# Check if already patched
if ($content -match "# Only define AccumulatorUnixServer if UnixStreamServer is available") {
    Write-Host "  File is already patched!"
}
else {
    Write-Host "  Applying patch..."
    
    # Find and replace the AccumulatorUnixServer class definition
    $oldPattern = "class AccumulatorUnixServer\(socketserver\.UnixStreamServer\):"
    $newPattern = @"
# Only define AccumulatorUnixServer if UnixStreamServer is available (not on Windows)
if hasattr(socketserver, 'UnixStreamServer'):
    class AccumulatorUnixServer(socketserver.UnixStreamServer):
"@
    
    # Replace the class definition line
    $content = $content -replace "class AccumulatorUnixServer\(socketserver\.UnixStreamServer\):", $newPattern
    
    # Now we need to indent the class body and add the else clause
    # This is complex, so let's use a different approach - read line by line
    
    $lines = Get-Content $accumulatorsPath
    $newLines = @()
    $inClass = $false
    $classIndentLevel = 0
    $i = 0
    
    foreach ($line in $lines) {
        if ($line -match "^class AccumulatorUnixServer\(socketserver\.UnixStreamServer\):") {
            # Add the conditional wrapper
            $newLines += ""
            $newLines += "# Only define AccumulatorUnixServer if UnixStreamServer is available (not on Windows)"
            $newLines += "if hasattr(socketserver, 'UnixStreamServer'):"
            $newLines += "    class AccumulatorUnixServer(socketserver.UnixStreamServer):"
            $inClass = $true
            $classIndentLevel = 4  # Original class content will be indented by 4 more spaces
        }
        elseif ($inClass) {
            # Check if we've reached the end of the class (next function or class definition)
            if ($line -match "^def " -or ($line -match "^class " -and $line -notmatch "AccumulatorUnixServer")) {
                # End of class, add else clause
                $newLines += "else:"
                $newLines += "    # On Windows, UnixStreamServer doesn't exist, so create a dummy class"
                $newLines += "    AccumulatorUnixServer = None  # type: ignore[assignment,misc]"
                $newLines += ""
                $newLines += $line
                $inClass = $false
            }
            elseif ($line -match "^\s*$") {
                # Empty line
                $newLines += $line
            }
            else {
                # Class content - add extra indentation
                $newLines += "    " + $line
            }
        }
        else {
            $newLines += $line
        }
        $i++
    }
    
    # Write the patched content
    $newLines | Set-Content $accumulatorsPath -Encoding UTF8
    Write-Host "  Patch applied successfully!"
}

Write-Host "`nStep 4: Creating new pyspark.zip..."
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

# Compress the directory back to zip
Compress-Archive -Path "$extractPath\*" -DestinationPath $zipPath -Force
Write-Host "  New pyspark.zip created"

Write-Host "`nStep 5: Cleaning up..."
Remove-Item $extractPath -Recurse -Force
Write-Host "  Temporary files removed"

Write-Host "`n=== PATCH COMPLETED SUCCESSFULLY ==="
Write-Host "The pyspark.zip file has been patched for Windows compatibility."
Write-Host "Original backup saved at: $backupPath"
