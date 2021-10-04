Unicode True
!define APP_NAME "Open Gateway"
!define APP_PUBLISHER "SensiML Corporation"

; main executable relative to INSTDIR
!define APP_EXE "open-gateway.exe"
!define INSTDIR_REG_ROOT "HKCU"
!define INSTDIR_REG_KEY "Software\${APP_PUBLISHER}\${APP_NAME}"

!define NOREDIST

!define MUI_HEADERIMAGE
!define MUI_PAGE_HEADER_TEXT "${APP_NAME}"
!define MUI_ICON "img/icon.ico"

!ifdef VERSION_STRING
  VIProductVersion "${VERSION_STRING}"
!else
  VIProductVersion "2021.6.0.0"
!endif

VIAddVersionKey ProductName      "${APP_NAME}"
VIAddVersionKey Comments         ""
VIAddVersionKey CompanyName      "${APP_PUBLISHER}"
VIAddVersionKey LegalCopyright   "2021 ${APP_PUBLISHER}"
VIAddVersionKey FileDescription  "Installer for SensiML Open Gateway"
VIAddVersionKey FileVersion      1
VIAddVersionKey ProductVersion   1
VIAddVersionKey InternalName     "ogw"

!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Start Open Gateway"
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchOGW"

!define MUI_FINISHPAGE_SHOWREADME
!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Create Desktop Shortcut"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION "Shortcut"

!include MUI2.nsh
!include LogicLib.nsh
!include StrFunc.nsh
; Install AdvUninstLog from http://nsis.sourceforge.net/Advanced_Uninstall_Log_NSIS_Header
!include AdvUninstLog.nsh
!include x64.nsh

!insertmacro INTERACTIVE_UNINSTALL

Name "${APP_NAME}"
OutFile "dist/SensiML_OpenGateway_Setup.exe"

InstallDir "$PROGRAMFILES64\${APP_PUBLISHER}\${APP_NAME}"
InstallDirRegKey ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "InstallDir"
RequestExecutionLevel Admin
BrandingText "Open Gateway"


;Pages
!define MUI_PAGE_CUSTOMFUNCTION_PRE "PagePre"
!insertmacro MUI_PAGE_WELCOME

!insertmacro MUI_PAGE_LICENSE "LICENSE"
;!insertmacro MUI_PAGE_COMPONENTS

!define MUI_PAGE_CUSTOMFUNCTION_PRE "PagePre"
!insertmacro MUI_PAGE_DIRECTORY

!insertmacro MUI_PAGE_INSTFILES

!define MUI_PAGE_CUSTOMFUNCTION_PRE "FinishPagePre"
!define MUI_PAGE_CUSTOMFUNCTION_SHOW "FinishPageShow"
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; Variables
Var Update
Var DesktopShortcut

!finalize 'SignTool.exe sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a "%1"'

;Installer Sections

;Uninstall old version when upgrading
Section "" SecUninstallPrev
  SectionIn RO
  ReadRegStr $0 ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "InstallDir"
  StrCmp $0 "" done

  ${If} $Update = 1
    ExecWait '"$0\Uninstall.exe" /U /S _?=$0'
  ${Else}
    ExecWait '"$0\Uninstall.exe" /S _?=$0'
  ${EndIf}
  Delete "$0\Uninstall.exe"
  RMDir "$0"
  done:
SectionEnd

Section "Open Gateway" SecOGW
  SectionIn RO
  SetOutPath "$INSTDIR"

  !ifdef SRC_FOLDER

  !else
    !define SRC_FOLDER "dist"
  !endif

  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  ;START FILES
  File /r /x SensiML_OpenGateway_Setup.exe dist\*
  ;END FILES
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL

  ;Shortcuts
  CreateDirectory "$SMPROGRAMS\${APP_PUBLISHER}"
  CreateShortCut "$SMPROGRAMS\${APP_PUBLISHER}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
  CreateShortCut "$SMPROGRAMS\${APP_PUBLISHER}\Uninstall ${APP_NAME}.lnk" "$INSTDIR\Uninstall.exe"

  ;Store installation folder
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "InstallDir" $INSTDIR
  ;Add/Remove Programs Config
  WriteRegStr ${INSTDIR_REG_ROOT} "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
  WriteRegStr ${INSTDIR_REG_ROOT} "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\${APP_EXE},0"
  WriteRegStr ${INSTDIR_REG_ROOT} "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr ${INSTDIR_REG_ROOT} "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
SectionEnd

Function .onInit
  SetRegView 64
  Call IsUpdate
  ReadRegDWORD $DesktopShortcut ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "DesktopShortcut"
  !insertmacro UNINSTALL.LOG_PREPARE_INSTALL
FunctionEnd

Function .onInstSuccess
  !insertmacro UNINSTALL.LOG_UPDATE_INSTALL
FunctionEnd

Section Uninstall
  !insertmacro UNINSTALL.LOG_UNINSTALL "$INSTDIR"
  ;!insertmacro UNINSTALL.LOG_UNINSTALL "$APPDATA\${APP_NAME}"
  !insertmacro UNINSTALL.LOG_END_UNINSTALL

  ;Do not delete shortcuts or registry settings if upgrading
  ${Unless} $Update = 1
    Delete "$SMPROGRAMS\${APP_PUBLISHER}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_PUBLISHER}\Uninstall ${APP_NAME}.lnk"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    ;Delete Intel Start menu folder ONLY if empty
    RMDir "$SMPROGRAMS\${APP_PUBLISHER}"

    DeleteRegKey /ifempty ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}"
    DeleteRegKey ${INSTDIR_REG_ROOT} "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  ${EndUnless}
SectionEnd

Function un.onInit
  SetRegView 64
  Call un.IsUpdate
  !insertmacro UNINSTALL.LOG_BEGIN_UNINSTALL
FunctionEnd

;use macro to share function accross un/installer
!macro IsUpdate un
Function ${un}IsUpdate
  ClearErrors
  ${GetParameters} $0
  ${GetOptions} $0 "/U" $1
  IfErrors +2
  StrCpy $Update 1
FunctionEnd
!macroend
!insertmacro IsUpdate ""
!insertmacro IsUpdate "un."

Function LaunchOGW
  ExecShell "" "$INSTDIR\${APP_EXE}"
FunctionEnd

Function Shortcut
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
  WriteRegDWORD ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "DesktopShortcut" 1
FunctionEnd

;Skip Page if we've run with /U flag
Function PagePre
  ${If} $Update = 1
    Abort
  ${EndIf}
FunctionEnd

Function FinishPagePre
  ${If} $Update = 1
    Call LaunchOGW
    Abort
  ${EndIf}
FunctionEnd

Function FinishPageShow
  ${If} $DesktopShortcut = 1
    SendMessage $mui.FinishPage.ShowReadme ${BM_SETCHECK} ${BST_CHECKED} 0
  ${EndIf}
FunctionEnd
