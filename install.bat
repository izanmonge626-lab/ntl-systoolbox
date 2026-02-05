@echo off
setlocal EnableExtensions

REM ==========================================================
REM  NTL-SysToolbox - FULL Install + Run (Windows CMD)
REM  - Installe Nmap (silent)
REM  - Installe Npcap (interactive: pas de silent en version free)
REM  - Cree venv + installe requirements
REM  - Copie config.example.json -> config.json si absent
REM  - Lance run.bat (si present) sinon python src\main.py
REM ==========================================================

REM 0) Se placer a la racine du repo (dossier du .bat)
cd /d "%~dp0"

echo.
echo =========================
echo 1/8 Verification du repo
echo =========================
if not exist "requirements.txt" (
  echo [ERREUR] requirements.txt introuvable. Lance ce .bat a la racine du depot.
  pause
  exit /b 1
)
if not exist "src\main.py" (
  echo [ERREUR] src\main.py introuvable. Structure projet inattendue.
  pause
  exit /b 1
)
if not exist "config\" (
  echo [ERREUR] Dossier config\ introuvable.
  pause
  exit /b 1
)

echo.
echo =========================
echo 2/8 Verification admin
echo =========================
net session >nul 2>&1
if errorlevel 1 (
  echo [ERREUR] Lance ce .bat en tant qu'Administrateur :
  echo Clic droit ^> Executer en tant qu'administrateur
  pause
  exit /b 1
)

echo.
echo =========================
echo 3/8 Verification Python
echo =========================
where python >nul 2>&1
if errorlevel 1 (
  echo [ERREUR] Python introuvable. Installe Python et coche "Add Python to PATH".
  pause
  exit /b 1
)

echo.
echo =========================
echo 4/8 Installation Nmap (silent)
echo =========================
where nmap >nul 2>&1
if errorlevel 1 (
  echo Nmap introuvable. Telechargement + installation...
  set "NMAP_VER=7.98"
  set "NMAP_EXE=%TEMP%\nmap-%NMAP_VER%-setup.exe"

  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Invoke-WebRequest -Uri 'https://nmap.org/dist/nmap-%NMAP_VER%-setup.exe' -OutFile '%NMAP_EXE%'"

  if not exist "%NMAP_EXE%" (
    echo [ERREUR] Telechargement Nmap KO.
    pause
    exit /b 1
  )

  "%NMAP_EXE%" /S
)

where nmap >nul 2>&1
if errorlevel 1 (
  echo [ERREUR] Nmap toujours introuvable apres install.
  echo -> Redemarre Windows puis relance ce .bat.
  pause
  exit /b 1
)
echo OK: Nmap disponible.

echo.
echo =========================
echo 5/8 Installation Npcap (INTERACTIF)
echo =========================
if not exist "%WINDIR%\System32\Npcap" (
  echo Npcap introuvable.
  echo IMPORTANT: l'installation silencieuse n'est pas dispo en version gratuite.
  echo L'installeur va s'ouvrir : coche "WinPcap API-compatible mode" si propose.
  set "NPCAP_VER=1.87"
  set "NPCAP_EXE=%TEMP%\npcap-%NPCAP_VER%.exe"

  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Invoke-WebRequest -Uri 'https://npcap.com/dist/npcap-%NPCAP_VER%.exe' -OutFile '%NPCAP_EXE%'"

  if not exist "%NPCAP_EXE%" (
    echo [ERREUR] Telechargement Npcap KO.
    pause
    exit /b 1
  )

  "%NPCAP_EXE%"

  echo.
  echo (Si tu viens d'installer Npcap, attends la fin puis reviens ici.)
)

if not exist "%WINDIR%\System32\Npcap" (
  echo [ERREUR] Npcap toujours absent. Sans Npcap, Scapy/capture peut ne pas marcher.
  echo -> Installe Npcap puis relance ce .bat.
  pause
  exit /b 1
)
echo OK: Npcap verifie.

echo.
echo =========================
echo 6/8 Creation + activation venv
echo =========================
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  if errorlevel 1 (
    echo [ERREUR] Echec creation venv.
    pause
    exit /b 1
  )
)
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [ERREUR] Activation venv impossible.
  pause
  exit /b 1
)

echo.
echo =========================
echo 7/8 Installation dependances Python
echo =========================
python -m pip install --upgrade pip
if errorlevel 1 (
  echo [ERREUR] pip KO. Essaie: python -m ensurepip --upgrade
  pause
  exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERREUR] Installation requirements KO.
  pause
  exit /b 1
)

echo.
echo =========================
echo 8/8 Configuration + Lancement
echo =========================
if not exist "config\config.json" (
  if exist "config\config.example.json" (
    copy /Y "config\config.example.json" "config\config.json" >nul
    echo OK: config\config.json cree.
  ) else (
    echo [ERREUR] config\config.example.json introuvable.
    pause
    exit /b 1
  )
) else (
  echo OK: config\config.json existe deja (on ne touche pas).
)

echo.
echo Ouvre la config si besoin:
echo   notepad config\config.json
echo.

REM Lancement recommande
if exist "run.bat" (
  call "run.bat"
) else (
  python "src\main.py"
)

echo.
pause
endlocal