@setlocal
@pushd %~dp0../..
@ECHO off
rem ---------------------------------

set PROJECT_NAME=smash
set CMD=rmdir /S /Q
@ECHO on

%CMD% tests\.cache
%CMD% tests\__tmp__
%CMD% tests\__pycache__
%CMD% tests\%PROJECT_NAME%\__pycache__

%CMD% %PROJECT_NAME%\__pycache__

@ECHO off
rem ---------------------------------
@popd
endlocal
