# Expense Tracker App

A simple expense tracker application built with Kivy and KivyMD that can be compiled to an Android APK using Buildozer.

## Features

- ✅ **Add & Manage Expenses** - Track expenses with amount, category, and optional notes
- ✅ **View Expenses** - Display all expenses in an organized list with dates
- ✅ **Multi-Select Delete** - Select multiple expenses and delete them in batch
- ✅ **Calculate Totals** - Automatically calculate and display total expenses
- ✅ **Multi-Language Support** - Available in English, Amharic, and Oromo
- ✅ **Data Persistence** - All data stored locally using TinyDB (JSON-based)
- ✅ **Export Data** - Export expenses to file for backup or analysis
- ✅ **Input Validation** - Safe parsing and validation of expense data
- ✅ **Comprehensive Tests** - Unit tests for all core functionality

## Installation

### Requirements
- Python 3.10+
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/wish628/Expensive-Tracker-apk.git
   cd Expensive-Tracker-apk
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Desktop (Development)

```bash
python main.py
```

The app will start with the UI available. You can:
- Add expenses
- Switch languages (English / Amharic / Oromo)
- Delete single or multiple expenses
- Export data

### Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_translations_only.py       # Translation tests
pytest tests/test_utils.py                   # Validation function tests
pytest tests/test_db.py                      # Database tests
pytest tests/test_desktop_validation.py      # Desktop environment tests

# Run with verbose output
pytest tests/ -v
```

**Test Coverage:**
- 19 tests pass (1 skipped)
- Database operations (CRUD)
- Validation and error handling
- Translation loading for all 3 languages
- App structure and configuration validation

### Code Quality

The project uses automated code formatting and linting:

```bash
# Format code with autopep8
autopep8 --in-place main.py utils.py

# Check code style with flake8
flake8 main.py utils.py
```

## Multi-Language Support

The app supports three languages with complete translations:

| Language | Code | Status |
|----------|------|--------|
| English | `en` | ✅ Complete |
| Amharic | `am` | ✅ Complete |
| Oromo | `om` | ✅ Complete |

Switch languages using the language button in the app (EN/AM/OM).

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes and add tests if needed
4. Run the test suite to ensure nothing breaks
5. Commit your changes (`git commit -am 'Add your feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Open a Pull Request

### Code Standards

- Follow PEP 8 style guidelines (enforced with flake8)
- Write tests for new features
- Keep the translation files updated for all 3 languages

## Building for Android

This application is designed to be built into an Android APK using Buildozer on WSL (Windows Subsystem for Linux).

### Prerequisites

1. Install WSL with Ubuntu:
   ```
   wsl --install
   ```

2. In your Ubuntu terminal, update the system:
   ```
   sudo apt update && sudo apt upgrade -y
   ```

3. Install required dependencies:
   ```
   sudo apt install python3-pip build-essential git python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev -y
   ```

4. Install Buildozer:
   ```
   pip install --user buildozer
   ```

5. Install additional Android SDK/NDK tools:
   ```
   sudo apt install openjdk-17-jdk -y
   ```

### Building the APK

1. Navigate to your project folder in WSL:
   ```
   cd /mnt/c/Users/YourName/Desktop/exp
   ```

2. Initialize Buildozer (if not already done):
   ```
   buildozer init
   ```

3. Build the APK:
   ```
   buildozer -v android debug
   ```

The first build will take 10-30 minutes as it downloads the Android SDK, NDK, and Python for Android.

The APK will be located in the `bin/` folder: `bin/expense_tracker-1.0-debug.apk`

## Continuous Integration (optional)

A GitHub Actions workflow is included to build the APK in CI. Push to the `main` branch or run the workflow manually to start a build on GitHub-hosted runners. The workflow will attempt to install system packages, run Buildozer and upload the resulting APK as an artifact.

Notes:
- CI builds are long-running (first run downloads Android SDK/NDK and toolchains) and may require a runner timeout increase.
- The workflow file is `.github/workflows/build-apk.yml` in the repository.

CI trigger: this file was edited automatically to trigger a CI build for the Android APK.

### Installing the APK

You can install the APK on your Android device by:

1. Copying it to your phone and opening it, or
2. Using ADB:
   ```
   adb install bin/expense_tracker-1.0-debug.apk
   ```

## License

This project is open source and available under the MIT License.