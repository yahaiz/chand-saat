import os
import sys
import zipfile
import subprocess
import shutil

VERSION = "0.2.1"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist", "ChandSaat")
OUTPUT_DIR = os.path.join(BASE_DIR, "installer")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 1. Re-build with PyInstaller using current Python environment
print(f"Building PyInstaller EXE for version {VERSION}...")
spec_path = os.path.join(BASE_DIR, "ChandSaat.spec")
pyinstaller_cmd = [sys.executable, "-m", "PyInstaller", spec_path, "--noconfirm"]
subprocess.run(pyinstaller_cmd, check=True, cwd=BASE_DIR)

# 2. Find and execute Inno Setup compiler (ISCC.exe)
def find_inno_compiler():
    # Check PATH first
    path_iscc = shutil.which("iscc") or shutil.which("ISCC.exe")
    if path_iscc:
        return path_iscc

    # Common Windows installation locations
    candidate_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Inno Setup 6", "ISCC.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Inno Setup 6", "ISCC.exe"),
        os.path.join(os.environ.get("ProgramFiles", ""), "Inno Setup 6", "ISCC.exe")
    ]
    for p in candidate_paths:
        if p and os.path.exists(p):
            return p
    return None

inno_compiler = find_inno_compiler()
if inno_compiler:
    print(f"Found Inno Setup Compiler at: {inno_compiler}")
    print(f"Building Windows Setup Installer (ChandSaat_Setup_v{VERSION}.exe)...")
    iss_path = os.path.join(BASE_DIR, "setup.iss")
    subprocess.run([inno_compiler, iss_path], check=True, cwd=BASE_DIR)
else:
    print("WARNING: Inno Setup compiler (ISCC.exe) not found. Skipping Setup.exe creation.")

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
