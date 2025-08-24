# 🎯 Google Maps Business Profile Scraper

A professional tool for extracting Google Maps Business (GMB) profiles from mobile home parks across all 50 US states.

## ✨ Features

- 🎯 Scrape GMB profiles from all 50 US states
- 🌍 County-based data extraction
- 📊 Excel output format
- Powered by Hastylead
- 💳 Credit tracking system
- 🔒 Proxy support

## �� Quick Start

---

## �� WINDOWS GUIDE

### Option 1: Run with Python (Windows)

**Step 1: Install Python**
1. Go to [python.org](https://python.org)
2. Download Python 3.7+ for Windows
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Click "Install Now"

**Step 2: Verify Installation**
1. Open Command Prompt (Press `Win + R`, type `cmd`, press Enter)
2. Type: `python --version`
3. You should see: `Python 3.x.x`
4. Type: `pip --version`
5. You should see: `pip x.x.x`

**Step 3: Download Project**
1. Open Command Prompt
2. Navigate to your desired folder: `cd C:\Users\YourName\Desktop`
3. Clone the repository:
   ```cmd
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   ```
4. Enter the folder:
   ```cmd
   cd Google-map-bussniess
   ```

**Step 4: Install Dependencies**
```cmd
pip install -r requirements.txt
```

**Step 5: Run the Application**
```cmd
python main.py
```

### Option 2: Build Windows Executable (.exe)

**Step 1: Install PyInstaller**
1. Open Command Prompt in the project folder
2. Install PyInstaller:
   ```cmd
   pip install pyinstaller
   ```

**Step 2: Build Executable**
```cmd
pyinstaller --onefile --add-data "settings.ini;." --console --name "GMB_Scraper" main.py
```

**Step 3: Find Your Executable**
1. Look in the `dist` folder
2. You'll find `GMB_Scraper.exe`
3. Double-click to run

**🎯 One-Click Build (Windows):**
Simply double-click `build.bat` and wait for completion!

### Windows Troubleshooting

**Python not found:**
1. Reinstall Python and check "Add to PATH"
2. Or manually add: `C:\Users\YourUser\AppData\Local\Programs\Python\Python3x\`

**Import Errors:**
```cmd
pyinstaller --onefile --hidden-import=scrapy --hidden-import=scrapy.selector --hidden-import=pandas --hidden-import=requests --add-data "settings.ini;." --name "GMB_Scraper" main.py
```

---

## 🍎 macOS GUIDE

### Option 1: Run with Python (macOS)

**Step 1: Install Python**
1. Go to [python.org](https://python.org)
2. Download Python 3.7+ for macOS
3. Run the installer
4. Follow the installation wizard

**Step 2: Verify Installation**
1. Open Terminal (Applications → Utilities → Terminal)
2. Type: `python3 --version`
3. You should see: `Python 3.x.x`
4. Type: `pip3 --version`
5. You should see: `pip x.x.x`

**Step 3: Download Project**
1. Open Terminal
2. Navigate to your desired folder: `cd ~/Desktop`
3. Clone the repository:
   ```bash
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   ```
4. Enter the folder:
   ```bash
   cd Google-map-bussniess
   ```

**Step 4: Install Dependencies**
```bash
pip3 install -r requirements.txt
```

**Step 5: Run the Application**
```bash
python3 main.py
```

### Option 2: Build macOS Application (.app)

**Step 1: Install PyInstaller**
1. Open Terminal in the project folder
2. Install PyInstaller:
   ```bash
   pip3 install pyinstaller
   ```

**Step 2: Build Application**
```bash
python3 -m PyInstaller --windowed --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

**Step 3: Find Your Application**
1. Look in the `dist` folder
2. You'll find `GMB_Scraper.app`
3. Double-click to run

**Alternative - Single Executable:**
```bash
python3 -m PyInstaller --onefile --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

### macOS Troubleshooting

**Permission Denied:**
```bash
chmod +x dist/GMB_Scraper
```

**Python3 not found:**
1. Add to `~/.zshrc` or `~/.bash_profile`:
   ```bash
   export PATH="/usr/local/bin:$PATH"
   export PATH="/opt/homebrew/bin:$PATH"
   ```
2. Restart Terminal

**Gatekeeper Security:**
1. Go to **System Preferences** → **Security & Privacy**
2. Click **"Open Anyway"** for the GMB_Scraper app

---

## 🐧 LINUX GUIDE

### Option 1: Run with Python (Linux)

**Step 1: Install Python (Ubuntu/Debian)**
1. Open Terminal
2. Update package list:
   ```bash
   sudo apt update
   ```
3. Install Python and pip:
   ```bash
   sudo apt install python3 python3-pip git
   ```

**Step 1: Install Python (CentOS/RHEL)**
```bash
sudo yum install python3 python3-pip git
```

**Step 1: Install Python (Fedora)**
```bash
sudo dnf install python3 python3-pip git
```

**Step 2: Verify Installation**
1. Type: `python3 --version`
2. You should see: `Python 3.x.x`
3. Type: `pip3 --version`
4. You should see: `pip x.x.x`

**Step 3: Download Project**
1. Navigate to your desired folder: `cd ~/Desktop`
2. Clone the repository:
   ```bash
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   ```
3. Enter the folder:
   ```bash
   cd Google-map-bussniess
   ```

**Step 4: Install Dependencies**
```bash
pip3 install -r requirements.txt
```

**Step 5: Run the Application**
```bash
python3 main.py
```

### Option 2: Build Linux Binary

**Step 1: Install PyInstaller**
1. Open Terminal in the project folder
2. Install PyInstaller:
   ```bash
   pip3 install pyinstaller
   ```

**Step 2: Build Binary**
```bash
pyinstaller --onefile --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

**Step 3: Make Executable**
```bash
chmod +x dist/GMB_Scraper
```

**Step 4: Run**
```bash
./dist/GMB_Scraper
```

### Linux Troubleshooting

**Permission Denied:**
```bash
chmod +x dist/GMB_Scraper
```

**Missing Dependencies:**
```bash
# Ubuntu/Debian
sudo apt install python3-dev build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

---

## 🖥️ GUI Builder (All Platforms)

### Windows
1. Open Command Prompt in project folder
2. Install GUI tool:
   ```cmd
   pip install auto-py-to-exe
   ```
3. Run GUI:
   ```cmd
   auto-py-to-exe
   ```

### macOS
1. Open Terminal in project folder
2. Install GUI tool:
   ```bash
   pip3 install auto-py-to-exe
   ```
3. Run GUI:
   ```bash
   python3 -m auto_py_to_exe
   ```

### Linux
1. Open Terminal in project folder
2. Install GUI tool:
   ```bash
   pip3 install auto-py-to-exe
   ```
3. Run GUI:
   ```bash
   python3 -m auto_py_to_exe
   ```

**GUI Settings (All Platforms):**
- **Script Location**: Select `main.py`
- **Onefile**: Choose "One File"
- **Console Window**: Choose "Window Based"
- **Additional Files**: Add `settings.ini`
- **Click "Convert"**

---

## 📁 File Structure

- `main.py` - 🚀 Main application entry point
- `Google.py` - 🌐 Core scraping functionality
- `counties_data.py` - 🗺️ County data for all states
- `credit_tracker.py` - 💳 Credit management system
- `Utils.py` - Utility functions
- `requirements.txt` - 📦 Python dependencies
- `settings.ini` - ⚙️ Configuration file
- `build.bat` - 🎯 One-click build script (Windows)
- `Output/` - 📊 Generated Excel files

## ⚙️ System Requirements

### Windows
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum
- **Storage**: 500MB free space

### macOS
- **OS**: macOS 10.14 (Mojave) or later
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum
- **Storage**: 500MB free space

### Linux
- **OS**: Ubuntu 18.04+, CentOS 7+, Fedora 28+
- **Python**: 3.7 or higher
- **RAM**: 4GB minimum
- **Storage**: 500MB free space

## 🎯 How It Works

1. **Select State**: Choose from all 50 US states
2. **County Selection**: Pick specific counties or all counties
3. **Data Extraction**: Automated scraping of GMB profiles
4. **Excel Export**: Clean, organized data output
5. **Credit Tracking**: Monitor your usage and limits

## Output Format

The tool generates Excel files with:
- Business names and contact information
- Addresses and locations
- Phone numbers and websites
- Business categories and ratings
- Operating hours and services

## 🔒 Security Features

- Proxy support for secure scraping
- Rate limiting to avoid detection
- User-agent rotation
- Session management

## 📞 Support

For issues, questions, or customizations:
- **Contact**: Via Upwork
- **Repository**: Check issues section
- **Documentation**: Refer to troubleshooting guide above

## 🔄 Updates

Stay updated with the latest features:
1. **Clone the repository** to get updates
2. **Check for new releases** regularly
3. **Follow the build process** to create updated executables

---

## 🚀 Ready to Start?

**Choose your platform above and follow the step-by-step guide!**

**Happy Scraping! 🎯**
