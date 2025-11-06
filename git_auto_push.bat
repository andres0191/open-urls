@echo off
title 🚀 Git Auto Commit & Push
color 0a

echo ==============================================
echo 🧠 SCRIPT AUTOMÁTICO DE GIT - Auto Commit & Push
echo ==============================================
echo.

REM Cambiar a la carpeta del proyecto
cd /d "D:\projects python\open urls"

REM Verificar si hay cambios pendientes
for /f "delims=" %%i in ('git status --porcelain') do set changes=%%i

if "%changes%"=="" (
    echo ✅ No hay cambios para commitear.
    echo ----------------------------------------------
    git status
    pause
    exit /b
)

REM Mostrar estado
echo 🧩 Archivos modificados detectados:
git status
echo ----------------------------------------------
echo.

REM Solicitar mensaje de commit
set /p mensaje=✍️  Escribe el mensaje del commit: 

REM Verificar si el usuario escribió algo
if "%mensaje%"=="" (
    echo ❌ Error: No escribiste un mensaje de commit.
    pause
    exit /b
)

echo.
echo 🔄 Agregando archivos...
git add .

echo 💾 Creando commit...
git commit -m "%mensaje%"

echo 🚀 Subiendo cambios a GitHub (rama main)...
git push origin main

echo.
echo ✅ Commit y push completados exitosamente.
echo ----------------------------------------------
pause