
function Fix-BCLs($sourcePath, $destPath, $doCopy) {
    if ($sourcePath.Name -ne $destPath.Name) {
        throw "Run ID in source and dest do not match"
    }
    
    if (!((Test-Path -PathType Container $sourcePath) -and (Test-Path -PathType Container $destPath))) {
        throw "Missing source/dest directories"
    }
    
    $bclValidationLog = "$destPath\checked_bcls.csv"
    if ((Test-Path "$sourcePath\checked_bcls.csv") -or !(Test-Path $bclValidationLog)) {
        throw "Source and dest directories seem to be swapped"
    }

    $logFile = "$destPath\fix_bcls.log"
    
    function Log($msg) {
        $timeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $msg = "[$timeStamp] $msg"

        Write-Output $msg
        Add-Content $logFile -Value $msg
    }
    
    Log "Source: $sourcePath"
    Log "Dest: $destPath"
    Log "Validation log: $bclValidationLog"

    $validationRecords = Get-Content -Path $bclValidationLog
    $nBcls = 0
    $nBclsFixed = 0

    foreach ($line in $validationRecords) {
        $splitLine = $line -split ","

        if ($splitLine[1] -notmatch "0") {
            $filePath = $splitLine[0] -Split "/"
            $lane = $filePath[0]
            $cycle = $filePath[1]
            $basename = $filePath[2]

            $sourceFile = "$sourcePath\Data\Intensities\BaseCalls\$lane\$cycle\$basename"
            $destDir = "$destPath\Data\Intensities\BaseCalls\$lane\$cycle"
            $destFile = "$destDir\$basename"

            if (!(($lane) -and ($cycle) -and ($basename) -and (Test-Path $sourceFile))) {
                Log "Found bad bcl file path in checked_bcls.csv: $sourceFile"
                throw "Bad bcl file path"
            }

            $nBclsFixed += 1
            Log "Recopying $sourceFile to $destFile"

            if ($doCopy) {
                if (!(Test-Path -PathType Container $destDir)) {
                    Log "Missing container directory $destDir - creating"
                    New-Item -ItemType Directory $destDir
                }
                Copy-Item $sourceFile $destFile
            }
        }
        $nBcls += 1
    }
    
    Log "Found $nBcls bcls, fixed $nBclsFixed"    
    if (!($doCopy)) {
        Log "Dry run enabled - no files were copied"
    }
}

Write-Output "fix_bcls.ps1 - enter inputs as prompted, or ctrl-C to quit."
$destPath = (Read-Host "Enter the path to the run to be fixed") | Get-Item
$sourcePath = (Read-Host "Enter the path to the local backup copy of the run") | Get-Item
$doCopy = (Read-Host "Enter 'Y' if file copying should be enabled (i.e, this is not a dry run)") -eq "Y"

Fix-Bcls -sourcePath $sourcePath -destPath $destPath -doCopy $doCopy
