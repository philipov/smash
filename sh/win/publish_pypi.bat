@setlocal
@ECHO off

set THIS_PATH=%~dp0
set PROJECT_PATH=%THIS_PATH%..\..
set PIP_CONFIG_FILE=C:\dev\secrets\pip.ini
@pushd %PROJECT_PATH%

rem -- ToDo: macro to obtain __version__
rem twine upload dist\smash-0.0.0.zip --comment "make python platform wheels"
twine upload %PROJECT_PATH%\dist\smash-0.0.0-py3-none-any.whl --comment "smash things together"

@popd
@endlocal
