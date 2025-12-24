# インストーラービルド (Inno Setup)

このプロジェクトは、ランタイムバンドルにPyInstallerを、Windowsインストーラーの作成にInno Setupを使用しています。

## 前提条件
- Windows マシン
- Inno Setup (6.x)
- Python 3.10+ とプロジェクトの依存関係がインストールされていること

## 1) PyInstallerバンドルをビルドする

```powershell
python -m pip install -r requirements.txt
pyinstaller build/pyinstaller.spec
```

これにより、`dist/DocxXlsxToMarkdown/` に one-dir バンドルが生成されます。

## 2) Inno Setupスクリプトを作成する

以下の内容で `installer/DocxXlsxToMarkdown.iss` を作成します:

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

## 3) インストーラーをビルドする

Inno Setup Compilerで `.iss` ファイルを開き、**Build** をクリックします。
インストーラーは `installer/output/DocxXlsxToMarkdown-setup.exe` に作成されます。

## 4) リリースフロー

- GitHub Actionsワークフローは、PyInstallerバンドルをビルドし、zipアーティファクトとしてアップロードします。
- インストーラー (`.exe`) を作成した後、対応するGitHub Releaseに添付します。
- これを自動化したい場合は、Windows上でInno Setupビルドステップを追加し、`.exe` をリリースアセットとしてアップロードします。
