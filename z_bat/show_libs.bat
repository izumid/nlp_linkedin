@echo off
TITLE PIP: LIST LIBRARIES

set "path_env=%~dp0..\.venv\Scripts"
echo Enviroment path: %path_env%

call "%path_env%\activate.bat"
python -m pip list
call "%path_env%\deactivate.bat"

pause