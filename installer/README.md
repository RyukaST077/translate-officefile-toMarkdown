# Installer Build (Inno Setup)

This project uses PyInstaller for the runtime bundle and Inno Setup for a Windows installer.

## Prerequisites
- Windows machine
- Inno Setup (6.x)
- Python 3.10+ with project dependencies installed

## 1) Build the PyInstaller bundle

```powershell
python -m pip install -r requirements.txt
pyinstaller build/pyinstaller.spec
```

This produces a one-dir bundle at `dist/DocxXlsxToMarkdown/`.

## 2) Create the Inno Setup script

Create `installer/DocxXlsxToMarkdown.iss` with content similar to:

```ini
#define MyAppName "DocxXlsxToMarkdown"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Organization"
#define MyAppExeName "DocxXlsxToMarkdown.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
Publisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer\output
OutputBaseFilename={#MyAppName}-setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\DocxXlsxToMarkdown\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
```

## 3) Build the installer

Open the `.iss` file in Inno Setup Compiler and click **Build**.
The installer will be created at `installer/output/DocxXlsxToMarkdown-setup.exe`.

## 4) Release flow

- The GitHub Actions workflow builds the PyInstaller bundle and uploads a zip artifact.
- After creating the installer (`.exe`), attach it to the corresponding GitHub Release.
- If you prefer to automate this, add an Inno Setup build step on Windows and upload the `.exe` as a release asset.
