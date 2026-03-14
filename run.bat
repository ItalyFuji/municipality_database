@echo off
echo [1/2] Extracting municipality data from PDF...
python 01_extract_from_JapanMunicipalityPDF.py
if errorlevel 1 (
    echo ERROR: Step 1 failed.
    pause
    exit /b 1
)

echo [2/2] Normalizing municipality database...
python 02_normalize_municipality.py
if errorlevel 1 (
    echo ERROR: Step 2 failed.
    pause
    exit /b 1
)

echo Done. Output: data_output/municipality_DB.csv
pause
