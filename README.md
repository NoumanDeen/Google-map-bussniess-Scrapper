# Google Maps Business Profile Scraper

A professional tool for extracting Google Maps Business (GMB) profiles from mobile home parks across all 50 US states.

## Features

- 🎯 Scrape GMB profiles from all 50 US states
- 🌍 County-based data extraction
- 📊 Excel output format
- �� Powered by Hastylead
- 💳 Credit tracking system
- 🔒 Proxy support

## Quick Start

### Option 1: Run with Python
1. Install Python 3.7+
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

### Option 2: Build Executable (.exe)

#### Prerequisites
- Python 3.7+ installed
- Git or download repository as ZIP

#### Build Steps
1. **Clone/Download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
4. **Build the executable:**
   ```bash
   pyinstaller --onefile --name "GMB_Scraper" main.py
   ```
5. **Find your executable** in the `dist` folder as `GMB_Scraper.exe`

## Alternative: GUI Builder

For users who prefer a graphical interface:

1. **Install the GUI tool:**
   ```bash
   pip install auto-py-to-exe
   ```

2. **Run the GUI:**
   ```bash
   auto-py-to-exe
   ```

3. **In the GUI:**
   - Script Location: Select `main.py`
   - Onefile: Choose "One File"
   - Console Window: Choose "Window Based"
   - Click "Convert"

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
pyinstaller --onefile --hidden-import=scrapy --hidden-import=scrapy.selector --hidden-import=pandas --hidden-import=requests --name "GMB_Scraper" main.py
```

**File Not Found:**
```bash
pyinstaller --onefile --add-data "settings.ini;." --name "GMB_Scraper" main.py
```

**Large Executable Size:**
This is normal - the .exe includes Python runtime and all dependencies.

## File Structure
