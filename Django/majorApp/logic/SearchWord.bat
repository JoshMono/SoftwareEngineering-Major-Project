@echo off
REM Usage: SearchWord.bat "full_file_path" "search_term"
 
setlocal EnableDelayedExpansion
 
set "file=%~1"
set "search=%~2"
set /a count=0
 
REM Read file line by line
for /f "usebackq tokens=* delims=" %%A in ("%file%") do (
    set "line=%%A"
    REM Split line into words
    for %%w in (!line!) do (
        call :tolower "%%w" word
        call :tolower "%search%" term
        if "!word!"=="!term!" (
            set /a count+=1
        )
    )
)
 
echo %count%
exit /b
 
REM Function: convert to lowercase
:tolower
setlocal EnableDelayedExpansion
set "str=%~1"
for %%L in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    set "str=!str:%%L=%%L!"
    set "str=!str:%%L=%%L!"
)
endlocal & set "%~2=%str%"
exit /b