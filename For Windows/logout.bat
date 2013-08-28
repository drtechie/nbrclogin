@echo off
taskkill /f /im nbrclogin.exe && (
  echo nbrclogin.exe terminated
) || (
  echo.
  echo.
  echo ATTENTION
  echo nbrclogin.exe COULD NOT BE TERMINATED.
  echo Process has already stopped OR
  echo TRY RUNNING AS ADMINISTRATOR
  echo If you don't have admin privileges, manually stop the process - CTRL+SHIFT+ESC
  echo.
  echo.
)
nbrclogin.exe logout
pause>nul