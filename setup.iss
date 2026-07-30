; ChandSaat - Inno Setup Script
#define MyAppName "ChandSaat"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "ChandSaat Team"
#define MyAppExeName "ChandSaat.exe"

[Setup]
AppId={{D37F8A12-88E4-4192-9C80-5F119C6A7840}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=g:\my-daily-log\installer
OutputBaseFilename=ChandSaat_Setup_v0.1.0
SetupIconFile=g:\my-daily-log\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "g:\my-daily-log\dist\ChandSaat\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "g:\my-daily-log\dist\ChandSaat\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
