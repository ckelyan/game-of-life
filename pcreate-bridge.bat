set pcpath=%1
set patname=%2
set curdir=%~dp0

if "%pcpath%" == "" (
    echo Please provide a path to the pcreate folder
    exit 1
)

if "%patname%" == "" (
    set patname=default
)

cd %pcpath%
py main.py %patname% ai %curdir%presets.json

cd %curdir%
py main.py %patname%