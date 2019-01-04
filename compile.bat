@ECHO OFF

goto :main

:compile_discon
cd %~1
call :compile_64bit %~2
call :compile_Win32 %~2
call :cleanup .
cd ..
exit /B 0

:compile_64bit
mkdir build_64
cd build_64
cmake .. -G"Visual Studio 15 2017 Win64"
cmake --build . --config Release
copy Release\%~1.dll ..\..\DISCON_DLLS\64bit\.
cd ..
exit /B 0

:compile_Win32
mkdir build_32
cd build_32
cmake .. -G"Visual Studio 15 2017"
cmake --build . --config Release
copy Release\%~1.dll ..\..\DISCON_DLLS\Win32\.
cd ..
exit /B 0

:cleanup
cd %~1
rmdir /s /Q build_64 build_32
exit /B 0


:main

: move into the ServoData directory
set scriptpath=%~dp0
set servodata=%scriptpath:~0,-1%
cd %servodata%

: create the directories for storing the compiled libraries
mkdir DISCON_DLLS\64bit
mkdir DISCON_DLLS\Win32

: configure and build
call :compile_discon DISCON Discon
call :compile_discon DISCON_ITI Discon_ITIBarge
call :compile_discon DISCON_OC3 Discon_OC3Hywind
