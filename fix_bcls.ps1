
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

    $bclsToFixSource = @()
    $bclsToFixDest = @()  # store the dirnames, since get-item crashes if prospective file doesn't exist
    foreach ($line in $validationRecords) {
        $nBcls += 1
        $splitLine = $line -split ","

        if ($splitLine[1] -notmatch "0") {
            $filePath = $splitLine[0] -Split "/"
            $lane = $filePath[0]
            $cycle = $filePath[1]
            $basename = $filePath[2]

            $sourceFile = "$sourcePath\Data\Intensities\BaseCalls\$lane\$cycle\$basename"
            $destDir = "$destPath\Data\Intensities\BaseCalls\$lane\$cycle"

            if (!(($lane) -and ($cycle) -and ($basename) -and (Test-Path $sourceFile))) {
                Log "Found bad bcl file path in checked_bcls.csv: $sourceFile"
                throw "Bad bcl file path"
            }

            $bclsToFixSource += $sourceFile
            $bclsToFixDest += $destDir
            Log "$sourceFile -> $destDir\$basename"
        }
    }
    
    $doCopy = (Read-Host "The above $($bclsToFixSource.Length) files will be copied. Enter 'Y' to proceed, or anything else to quit") -eq "Y"
    if ($doCopy) {
        Log "Recopying"
        for ($i = 0; $i -le $bclsToFixSource.Length - 1; $i++) {
            $sourceFile = Get-Item $bclsToFixSource[$i]
            $destDir = $bclsToFixDest[$i]

            if (!(Test-Path -PathType Container $destDir)) {
                Log "Missing container directory $destDir - creating"
                New-Item -ItemType Directory $destDir
            }
            Copy-Item $sourceFile "$destDir\$($sourceFiles.Name)"

            if (($i % 50) -eq 0) {
                Log "Recopied $i BCLs"
            }
        }
    } else {
        Log "Dry run - no files were copied"
    }
}

Write-Output "fix_bcls.ps1 - enter inputs as prompted, or ctrl-C to quit."
$destPath = (Read-Host "Enter the path to the run to be fixed") | Get-Item
$sourcePath = (Read-Host "Enter the path to the local backup copy of the run") | Get-Item

Fix-Bcls -sourcePath $sourcePath -destPath $destPath -doCopy $doCopy
