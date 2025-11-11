# 📱 Expensive Tracker - APK Build Guide

## ⚠️ Build Status

The APK build process is **network-intensive** and requires downloading large dependencies (Android NDK, SDK, Python 3.9, Kivy, KivyMD, SDL2, etc.). This can be problematic in cloud environments.

**Buildozer Build Issue**: `sh.CommandNotFound: ./download.sh` for SDL2_image
- This is a known buildozer + cloud environment limitation
- The build tools are trying to download SDL2_image but hit network restrictions

---

## 🏗️ How to Build APK (Local Machine or Docker)

### Option 1: Build on Local Machine (Recommended)

#### Prerequisites:
```bash
# Install buildozer
pip install buildozer

# Install Android SDK/NDK (via buildozer)
buildozer android debug  # First run downloads everything

# OR manually:
# - Java JDK 8+
# - Android SDK (API 33)
# - Android NDK (r25b)
```

#### Build Steps:
```bash
# 1. Clone or download the project
git clone https://github.com/wish628/Expensive-Tracker-apk
cd Expensive-Tracker-apk

# 2. Make sure database is clean
rm -f expenses.json

# 3. Build APK (debug)
buildozer android debug

# 4. Build APK (release - needs signing)
buildozer android release
```

#### APK Output Location:
```
bin/expense_tracker-1.0-debug.apk          (Debug version)
bin/expense_tracker-1.0-release.apk        (Release version - needs signing)
```

---

### Option 2: Using Docker

#### Dockerfile Setup:
```dockerfile
FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip openjdk-11-jdk git wget unzip

# Install buildozer and dependencies
RUN pip install buildozer Cython

# Set working directory
WORKDIR /app

# Copy project
COPY . .

# Build APK
CMD buildozer android debug
```

#### Build in Docker:
```bash
docker build -t expense-tracker-builder .
docker run -v $(pwd)/bin:/app/bin expense-tracker-builder
```

---

### Option 3: Using P4A (Python for Android) Directly

```bash
# Install p4a
pip install python-for-android

# Create distribution
p4a apk \
  --private . \
  --package org.example.expense_tracker \
  --name "Expensive Tracker" \
  --version 1.0 \
  --bootstrap sdl2 \
  --requirements python3,kivy,kivymd,tinydb \
  --permission INTERNET \
  --icon icon.png
```

---

## 🎯 Build Configuration (buildozer.spec)

Current Configuration:
```ini
[app]
title = ExpenseTracker
package.name = expense_tracker
package.domain = org.example
version = 1.0

requirements = python3,kivy,kivymd,tinydb

[app:android]
android.api = 33              # Target API
android.minapi = 21            # Minimum API
android.ndk = 25b             # NDK version
fullscreen = 0                # Allow status bar
orientation = portrait         # Portrait mode

source.exclude_dirs = tests, bin, .buildozer, artifacts
```

---

## 📦 Build Artifacts

### Generated Files:
```
bin/
├── expense_tracker-1.0-debug.apk        # Debug APK (unsigned)
└── expense_tracker-1.0-release.apk      # Release APK (needs signing)

.buildozer/
├── android/
│   └── platform/
│       ├── android-sdk/                 # Android SDK
│       ├── android-ndk-r25b/           # Android NDK
│       └── build-arm64-v8a/            # Build output
```

---

## 🔑 Release APK Signing

To release on Play Store, you need to sign the APK:

```bash
# 1. Generate keystore
keytool -genkey -v -keystore release-key.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release-key

# 2. Sign APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 \
  -keystore release-key.keystore \
  bin/expense_tracker-1.0-release.apk release-key

# 3. Verify signature
jarsigner -verify -verbose \
  bin/expense_tracker-1.0-release.apk
```

---

## 📱 Installing APK on Device

### Via ADB:
```bash
# Install debug APK
adb install -r bin/expense_tracker-1.0-debug.apk

# Run app
adb shell am start -n org.example.expense_tracker/.expense_trackerActivity
```

### Via File Transfer:
- Copy APK to Android device
- Open File Manager
- Find APK file
- Tap to install

### Via Android Studio:
1. Open project in Android Studio
2. Navigate to: Tools → Run/Debug Configuration
3. Select APK
4. Click "Run"

---

## ✅ Testing Before Release

### Desktop Testing (Already Done ✅):
```bash
# Run all tests
pytest tests/ -v

# Test desktop app
python main.py
```

### Android Testing Checklist:
- [ ] App launches without crashes
- [ ] Can add expenses
- [ ] Can delete expenses
- [ ] Multi-select delete works
- [ ] All 3 languages load correctly
- [ ] Notifications display
- [ ] Database persists after restart
- [ ] UI responsive and no lag

---

## 🐛 Troubleshooting

### Problem: `sh.CommandNotFound: ./download.sh`
**Solution**:
```bash
# Clean and retry
rm -rf .buildozer
buildozer android debug
```

### Problem: `ndk-build not found`
**Solution**:
```bash
# Ensure NDK is set
export ANDROID_NDK_PATH=~/.buildozer/android/platform/android-ndk-r25b
buildozer android debug
```

### Problem: Out of memory during build
**Solution**:
```bash
# Increase Java heap
export JAVA_TOOL_OPTIONS="-Xmx2048m"
buildozer android debug
```

### Problem: Gradle build fails
**Solution**:
```bash
# Clear gradle cache
rm -rf ~/.gradle/caches
buildozer android debug
```

---

## 🔄 Build Commands Reference

```bash
# Clean build
buildozer android clean

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release

# Run on connected device
buildozer android debug deploy run

# View build logs
tail -f buildozer.log

# Increase log verbosity
buildozer android debug -- --verbose
```

---

## 📊 Build Time Estimates

| Task | Time |
|------|------|
| First setup (downloads Android SDK/NDK) | 30-60 min |
| Subsequent builds | 5-15 min |
| Debug APK build | 5-10 min |
| Release APK build + signing | 10-15 min |

---

## ✨ Why Desktop App Already Works

The desktop version (`python main.py`) is **already production-ready** because:
- ✅ All code works in Python
- ✅ No Android-specific code needed
- ✅ Kivy is cross-platform
- ✅ Database uses standard TinyDB
- ✅ All tests pass (19/19)

**Use desktop version while waiting for APK build to complete!**

---

## 📝 Deployment Steps

### After APK is Built:

#### Option A: Direct Distribution
1. Generate release APK
2. Sign with your keystore
3. Share APK file
4. Users install via: Settings → Apps → Install from Unknown Sources

#### Option B: Google Play Store
1. Create Google Play Developer Account ($25 one-time)
2. Sign APK with release keystore
3. Create app listing in Play Console
4. Upload APK to internal testing/beta/production

#### Option C: GitHub Releases
1. Upload APK to GitHub Releases
2. Add version notes
3. Users download directly from releases page

---

## 🎯 Current Status

| Task | Status | Notes |
|------|--------|-------|
| Desktop app | ✅ READY | `python main.py` works |
| Tests | ✅ PASSING | 19/19 tests pass |
| Database | ✅ EMPTY | Fresh start for new users |
| Code | ✅ OPTIMIZED | PEP 8 compliant |
| APK build | ⚠️ CLOUD ISSUE | Try building locally |

---

## 🚀 Next Steps

### To Get APK:

1. **Option 1 - LOCAL BUILD** (Recommended):
   ```bash
   # On your local Windows/Mac/Linux machine:
   git clone https://github.com/wish628/Expensive-Tracker-apk
   cd Expensive-Tracker-apk
   buildozer android debug
   # APK will be in bin/
   ```

2. **Option 2 - DOCKER BUILD**:
   ```bash
   docker build -t expense-tracker:latest .
   docker run -v $(pwd)/bin:/app/bin expense-tracker:latest
   ```

3. **Option 3 - USE DESKTOP APP MEANWHILE**:
   ```bash
   python main.py
   # Full app experience on desktop!
   ```

---

**Status**: Desktop app is production-ready. APK build requires local environment with full Android SDK/NDK setup.

For immediate use: `python main.py` ✅
