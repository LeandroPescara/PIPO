[Setup]
AppName=PIPO
AppVersion=1.0
DefaultDirName={autopf}\PIPO
DefaultGroupName=PIPO
OutputBaseFilename=PIPO_Instalador
Compression=lzma
SolidCompression=yes
SetupIconFile=C:\Users\leas_\OneDrive\Desktop\pipo\pipoicono.ico
WizardStyle=modern
AppPublisher=Leandro Pescara
AppPublisherURL=https://github.com/LeandroPescara

[Files]
Source: "C:\Users\leas_\OneDrive\Desktop\pipo\dist\pipo.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\PIPO"; Filename: "{app}\pipo.exe"
Name: "{autodesktop}\PIPO"; Filename: "{app}\pipo.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear ícono en el Escritorio"; GroupDescription: "Opciones adicionales"

[Messages]
[Messages]
WelcomeLabel1=🎶 ¡Bienvenido a la instalación de PIPO!
WelcomeLabel2=Tu herramienta mágica para convertir videos en música. ¡Gracias por confiar en nosotros!
FinishedLabel=🎶 ¡PIPO fue instalado exitosamente! ¡Disfrutalo!


[Run]
Filename: "{app}\pipo.exe"; Description: "Lanzar PIPO ahora"; Flags: nowait postinstall skipifsilent


