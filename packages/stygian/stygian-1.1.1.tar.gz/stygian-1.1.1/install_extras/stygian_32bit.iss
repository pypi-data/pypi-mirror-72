[Setup]
AppName = Stygian
AppID = Suprock Tech Stygian
AppVersion = {#VERSION}
AppVerName = Stygian {#VERSION}
AppPublisher = Suprock Tech
AppPublisherURL = http://suprocktech.com/
CloseApplications = force
DefaultDirName = {autopf}\Stygian
DefaultGroupName = Stygian
DisableProgramGroupPage = yes
Compression = lzma2
SolidCompression = yes
OutputBaseFilename = Stygian 32-bit Setup
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp
SetupIconFile=stygian.ico

; Win Vista
MinVersion = 6.0

; This installation requires admin priviledges. This is needed to install
; drivers on windows vista and later.
PrivilegesRequired = admin

[InstallDelete]
; Remove library files from the last installation; this is the easiest way to allow deletions
Type: filesandordirs; Name: "{app}\lib"

[Files]
Source: "*"; DestDir: "{app}"; Excludes: "\*.iss,\*.ico,\*.bmp,\*.ini,\Output,lib\hyperborea\7zip_*,lib\asphodel\lib*"; Flags: recursesubdirs ignoreversion
Source: "lib\hyperborea\7zip_32bit\*"; DestDir: "{app}\lib\hyperborea\7zip_32bit"; Flags: ignoreversion
Source: "lib\asphodel\lib32\*.dll"; DestDir: "{app}\lib\asphodel\lib32"; Flags: ignoreversion
Source: "Stygian.ini"; DestDir: "{userappdata}\Suprock Tech"; Flags: onlyifdoesntexist

[Run]
Filename: "{app}\stygian.exe"; Description: "Launch Stygian"; Flags: postinstall nowait

[Icons]
Name: "{group}\Stygian (32-bit)"; Filename: "{app}\stygian.exe";
Name: "{group}\Stygian Update (32-bit)"; Filename: "{app}\stygian_update.exe"; Flags: excludefromshowinnewinstall

[Code]
(* This deletes the installer if run with /DeleteInstaller=Yes *)
procedure CurStepChanged(CurStep: TSetupStep);
var
  strContent: String;
  intErrorCode: Integer;
  strSelf_Delete_BAT: String;
begin
  if CurStep=ssDone then
  begin
    if ExpandConstant('{param:DeleteInstaller|No}') = 'Yes' then
    begin
      strContent := ':try_delete' + #13 + #10 +
            'del "' + ExpandConstant('{srcexe}') + '"' + #13 + #10 +
            'if exist "' + ExpandConstant('{srcexe}') + '" goto try_delete' + #13 + #10 +
            'del %0';
  
      strSelf_Delete_BAT := ExtractFilePath(ExpandConstant('{tmp}')) + 'SelfDelete.bat';
      SaveStringToFile(strSelf_Delete_BAT, strContent, False);
      Exec(strSelf_Delete_BAT, '', '', SW_HIDE, ewNoWait, intErrorCode);
    end;
  end;
end;
