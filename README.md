# 🎯 Google Maps Business Profile Scraper

A professional tool for extracting Google Maps Business (GMB) profiles from mobile home parks across all 50 US states.

## ✨ Features

- 🎯 Scrape GMB profiles from all 50 US states
- 🌍 County-based data extraction
- 📊 Excel output format
- Powered by Hastylead
- 💳 Credit tracking system
- 🔒 Proxy support

## 🚀 Quick Start

### Option 1: Run with Python (All Platforms)

#### Windows
1. **Install Python 3.7+** from [python.org](https://python.org)
   - Download Windows installer
   - Check "Add Python to PATH" during installation

2. **Open Command Prompt or PowerShell:**
   ```cmd
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   cd Google-map-bussniess
   pip install -r requirements.txt
   python main.py
   ```

#### macOS
1. **Install Python 3.7+** from [python.org](https://python.org)
   - Download macOS installer
   - Or use Homebrew: `brew install python3`

2. **Open Terminal:**
   ```bash
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   cd Google-map-bussniess
   pip3 install -r requirements.txt
   python3 main.py
   ```

#### Linux (Ubuntu/Debian)
1. **Install Python 3.7+:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git
   ```

2. **Clone and run:**
   ```bash
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   cd Google-map-bussniess
   pip3 install -r requirements.txt
   python3 main.py
   ```

#### Linux (CentOS/RHEL/Fedora)
1. **Install Python 3.7+:**
   ```bash
   # CentOS/RHEL
   sudo yum install python3 python3-pip git
   
   # Fedora
   sudo dnf install python3 python3-pip git
   ```

2. **Clone and run:**
   ```bash
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   cd Google-map-bussniess
   pip3 install -r requirements.txt
   python3 main.py
   ```

### Option 2: Build Executable

#### Windows (.exe)

**Prerequisites:**
- Python 3.7+ installed
- Git or download repository as ZIP

**Build Steps:**
1. **Clone/Download repository:**
   ```cmd
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   cd Google-map-bussniess
   ```
   *Or download as ZIP from: https://github.com/NoumanDeen/Google-map-bussniess*

2. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **Build executable:**
   ```cmd
   pyinstaller --onefile --add-data "settings.ini;." --console --name "GMB_Scraper" main.py
   ```

4. **Find your .exe** in the `dist` folder

**🎯 One-Click Build (Windows):**
Simply double-click `build.bat` and wait for the build to complete!

#### macOS (.app)

**Prerequisites:**
- macOS 10.14+ (Mojave or later)
- Python 3.7+ installed
- Git (usually pre-installed)

**Build Steps:**
1. **Open Terminal** (Applications → Utilities → Terminal)

2. **Install Homebrew** (if needed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install Python** (if needed):
   ```bash
   brew install python3
   ```

4. **Clone and build:**
   ```bash
   git clone https://github.com/NoumanDeen/Google-map-bussniess.git
   cd Google-map-bussniess
   pip3 install -r requirements.txt
   pip3 install pyinstaller
   python3 -m PyInstaller --windowed --add-data "settings.ini:." --name "GMB_Scraper" main.py
   ```

5. **Find your .app** in the `dist` folder

**Alternative - Single Executable:**
```bash
python3 -m PyInstaller --onefile --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

#### Linux (Binary)

**Prerequisites:**
- Python 3.7+ installed
- Git installed

**Ubuntu/Debian Build:**
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip git

# Clone and build
git clone https://github.com/NoumanDeen/Google-map-bussniess.git
cd Google-map-bussniess
pip3 install -r requirements.txt
pip3 install pyinstaller
pyinstaller --onefile --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

**CentOS/RHEL/Fedora Build:**
```bash
# Install dependencies
sudo yum install python3 python3-pip git  # CentOS/RHEL
# OR
sudo dnf install python3 python3-pip git  # Fedora

# Clone and build
git clone https://github.com/NoumanDeen/Google-map-bussniess.git
cd Google-map-bussniess
pip3 install -r requirements.txt
pip3 install pyinstaller
pyinstaller --onefile --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

**Arch Linux Build:**
```bash
# Install dependencies
sudo pacman -S python python-pip git

# Clone and build
git clone https://github.com/NoumanDeen/Google-map-bussniess.git
cd Google-map-bussniess
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

## 🖥️ GUI Builder (All Platforms)

### Windows
```cmd
pip install auto-py-to-exe
auto-py-to-exe
```

### macOS
```bash
pip3 install auto-py-to-exe
python3 -m auto_py_to_exe
```

### Linux
```bash
pip3 install auto-py-to-exe
python3 -m auto_py_to_exe
```

**GUI Settings (All Platforms):**
- **Script Location**: Select `main.py`
- **Onefile**: Choose "One File"
- **Console Window**: Choose "Window Based"
- **Additional Files**: Add `settings.ini`
- **Click "Convert"**

## 🔧 Platform-Specific Troubleshooting

### Windows Issues

**Import Errors:**
```cmd
pyinstaller --onefile --hidden-import=scrapy --hidden-import=scrapy.selector --hidden-import=pandas --hidden-import=requests --add-data "settings.ini;." --name "GMB_Scraper" main.py
```

**File Not Found:**
```cmd
pyinstaller --onefile --add-data "settings.ini;." --name "GMB_Scraper" main.py
```

**Python not in PATH:**
- Reinstall Python and check "Add to PATH"
- Or add manually: `C:\Users\YourUser\AppData\Local\Programs\Python\Python3x\`

### macOS Issues

**Permission Denied:**
```bash
chmod +x dist/GMB_Scraper
```

**Python3 not found:**
```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="/usr/local/bin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"
```

**Gatekeeper Security:**
- Go to **System Preferences** → **Security & Privacy**
- Click **"Open Anyway"** for the GMB_Scraper app

**M1/M2 Mac Issues:**
```bash
arch -x86_64 python3 -m PyInstaller --windowed --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

### Linux Issues

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

# Fedora
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

**Import Errors:**
```bash
pyinstaller --onefile --hidden-import=scrapy --hidden-import=scrapy.selector --hidden-import=pandas --hidden-import=requests --add-data "settings.ini:." --name "GMB_Scraper" main.py
```

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

### Windows Users
1. **Download** this repository
2. **Double-click** `build.bat` for one-click build
3. **Or follow** the manual build steps above

### macOS Users
1. **Open Terminal** and follow the macOS instructions
2. **Use `python3` and `pip3`** commands
3. **Build your .app** using PyInstaller

### Linux Users
1. **Open Terminal** and follow the Linux instructions
2. **Use `python3` and `pip3`** commands
3. **Build your binary** using PyInstaller

**Happy Scraping on Your Platform! 🎯**
