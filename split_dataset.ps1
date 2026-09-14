$zipsDir      = "cvat_exports"
$unzipTempDir = "cvat_exports_unzipped"
$datasetDir   = "dataset"
 
$frameStep   = 30
$bgKeepEvery = 6
$bgCounter   = 0
 
$testVideos = @(6, 19, 26, 37)
$valVideos  = @(12, 28, 34, 35)
 
$allVideoNumbers = 1..39
 
foreach ($num in $allVideoNumbers) {
 
    $numPadded = "{0:D2}" -f $num
    $zipName = "video_$numPadded.zip"
    $zipPath = Join-Path $zipsDir $zipName
 
    if (-Not (Test-Path $zipPath)) {
        Write-Host "UWAGA: nie znaleziono $zipPath - pomijam" -ForegroundColor Yellow
        continue
    }
 
    if ($testVideos -contains $num) {
        $split = "test"
    } elseif ($valVideos -contains $num) {
        $split = "val"
    } else {
        $split = "train"
    }
 
    $extractPath = Join-Path $unzipTempDir "video_$numPadded"
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
 
    $sourceDataDir = Join-Path $extractPath "obj_train_data"
 
    if (-Not (Test-Path $sourceDataDir)) {
        Write-Host "UWAGA: brak folderu obj_train_data w $zipName" -ForegroundColor Red
        continue
    }
 
    $destImages = Join-Path $datasetDir "images\$split"
    $destLabels = Join-Path $datasetDir "labels\$split"
 
    $copiedCount = 0
    Get-ChildItem -Path $sourceDataDir -Filter "*.png" | ForEach-Object {
 
        if ($_.BaseName -match '(\d+)$') {
            $frameNum = [int]$matches[1]
 
            if ($frameNum % $frameStep -eq 0) {
 
                $txtSource = Join-Path $sourceDataDir "$($_.BaseName).txt"
                $isEmpty = $true
                if (Test-Path $txtSource) {
                    $isEmpty = ((Get-Item $txtSource).Length -eq 0)
                }
 
                $shouldCopy = $true
 
                if ($split -eq "train" -and $isEmpty) {
                    $bgCounter++
                    if (($bgCounter % $bgKeepEvery) -ne 0) {
                        $shouldCopy = $false
                    }
                }
 
                if ($shouldCopy) {
                    $newImgName = "video_${numPadded}_$($_.Name)"
                    Copy-Item $_.FullName -Destination (Join-Path $destImages $newImgName)
 
                    if (Test-Path $txtSource) {
                        $newLblName = "video_${numPadded}_$($_.BaseName).txt"
                        Copy-Item $txtSource -Destination (Join-Path $destLabels $newLblName)
                    }
                    $copiedCount++
                }
            }
        }
    }
 
    Write-Host "video_$numPadded -> $split : skopiowano $copiedCount klatek" -ForegroundColor Green
}
 
Write-Host ""
Write-Host "GOTOWE. Podsumowanie:" -ForegroundColor Cyan
foreach ($split in @("train", "val", "test")) {
    $imgCount = (Get-ChildItem (Join-Path $datasetDir "images\$split") -Filter "*.png" -ErrorAction SilentlyContinue).Count
    $lblCount = (Get-ChildItem (Join-Path $datasetDir "labels\$split") -Filter "*.txt" -ErrorAction SilentlyContinue).Count
    Write-Host "$split : $imgCount obrazow, $lblCount etykiet"
}
