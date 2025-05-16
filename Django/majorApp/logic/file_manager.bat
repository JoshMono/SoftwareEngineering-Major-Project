@echo off
setlocal
 
:: @echo off
setlocal
 
:: ========================
:: SECTION 1: Handle Inputs
:: ========================
 
:: Get inputs from arguments
set folderName=%1
set fileName=%2
set fileContent=%~3   
:: Use ~ to handle quotes and spaces properly
 
:: ========================
:: SECTION 2: Create Folder
:: ========================
 
mkdir "%folderName%"
 
:: =======================
:: SECTION 3: Create File
:: =======================
 
echo %fileContent% > "%folderName%\%fileName%"
echo File '%fileName%' created inside '%folderName%'.
 
endlocal
