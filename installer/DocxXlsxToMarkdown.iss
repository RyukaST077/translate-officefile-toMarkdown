#define MyAppName "DocxXlsxToMarkdown"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "tester"
#define MyAppExeName "DocxXlsxToMarkdown.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
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