import os
import zipfile
import subprocess
import shutil

VERSION = "0.1.0"
DIST_DIR = r"g:\my-daily-log\dist\ChandSaat"
OUTPUT_DIR = r"g:\my-daily-log\installer"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 1. Re-build with PyInstaller
print(f"Building PyInstaller EXE for version {VERSION}...")
pyinstaller_cmd = [r"g:\my-daily-log\.venv\Scripts\pyinstaller.exe", "ChandSaat.spec", "--noconfirm"]
subprocess.run(pyinstaller_cmd, check=True)

# 2. Build Windows Installer (.exe Setup)
inno_compiler = r"C:\Users\ASUS\AppData\Local\Programs\Inno Setup 6\ISCC.exe"
if os.path.exists(inno_compiler):
    print(f"Building Windows Setup Installer (ChandSaat_Setup_v{VERSION}.exe)...")
    subprocess.run([inno_compiler, "setup.iss"], check=True)

# 3. Create Standalone ZIP Bundle
zip_filename = os.path.join(OUTPUT_DIR, f"ChandSaat_v{VERSION}_Portable.zip")
print(f"Packaging executable to ZIP bundle: {zip_filename}")

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(DIST_DIR):
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, os.path.dirname(DIST_DIR))
            zipf.write(abs_path, rel_path)

print(f"Package created successfully: {zip_filename}")
