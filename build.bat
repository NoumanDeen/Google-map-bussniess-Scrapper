@echo off
echo ========================================
echo    GMB Scraper - Build Script
echo ========================================
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --onefile --name "GMB_Scraper" main.py

echo Build completed successfully!
echo Your executable is in the 'dist' folder: GMB_Scraper.exe
pause
