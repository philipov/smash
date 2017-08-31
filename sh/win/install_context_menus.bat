@setlocal
@ECHO off
rem ---------------------------------

set PATH_THIS=%~dp0
set PATH_PROJECT=%PATH_THIS%..\..

set PYTHONPATH=%PATH_PROJECT%;%PYTHONPATH%
@pushd %PATH_PROJECT%


rem ---------------------------------

set CMD=example\register_context_menus.reg
echo "CMD" %CMD%
%CMD%

rem ---------------------------------
@popd
@endlocal
