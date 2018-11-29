
function Fix-BCLs ($sourcePath, $destPath, $doCopy)
{
    Get-Location
    Write-Output "source: $sourcePath"
    Write-Output "dest: $destPath"
    if ($sourcePath.Name -ne $destPath.Name) {
        throw "Run ID in source and dest do not match"
    }
    
    if (!(Test-Path -PathType Container $sourcePath) -and (Test-Path -PathType Container $destPath)) {
        throw "Missing source/dest directories"
    }

    $bclValidationLog = "$destPath\checked_bcls.csv"
    $validationRecords = Get-Content -Path $bclValidationLog

    $bclsToFix = @()
    foreach ($line in $validationRecords)
    {
        $splitLine = $line -split ","
        if ($splitLine[1] -notmatch "0") { $bclsToFix += $splitLine[0] }
    }
    $nBcls = $bclsToFix.Length
    Write-Output "Fixing $nBcls bcls"
    
    foreach ($filePath in $bclsToFix) {
        $filePath = $filePath -Split "/"
        $lane = $filePath[0]
        $cycle = $filePath[1]
        $basename = $filePath[2]
        
        $sourceFile = "$sourcePath\Data\Intensities\BaseCalls\$lane\$cycle\$basename"
        $destDir = "$destPath\Data\Intensities\BaseCalls\$lane\$cycle"
        $destFile = "$destDir\$basename"
        
        if (!(($lane) -and ($cycle) -and ($basename) -and (Test-Path $sourceFile))) {
            Write-Output "Found bad bcl file path in checked_bcls.csv: $sourceFile"
            throw "Bad bcl file path"
        }

        Write-Output "Recopying $sourceFile to $destFile"
        
        if ($doCopy) {
            if (!(Test-Path -PathType Container $destDir)) {
                Write-Output "Missing container directory $destDir - creating"
                New-Item -ItemType Directory $destDir
            }
            Copy-Item $sourceFile $destFile
        }
    }
    
    Write-Output "Fixed $nBcls bcls"    
    if (!($doCopy)) {
        Write-Output "Dry run enabled - no files were copied"
    }
}

$destPath = (Read-Host "Enter the path to the run to be fixed") | Get-Item
$sourcePath = (Read-Host "Enter the path to the local backup copy of the run") | Get-Item
$doCopy = (Read-Host "Enter 'Y' if file copying should be enabled (i.e, this is not a dry run)") -eq "Y"

Fix-Bcls -sourcePath $sourcePath -destPath $destPath -doCopy $doCopy
