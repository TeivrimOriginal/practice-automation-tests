@echo off
setlocal
if exist .venv\Scripts\python.exe (
  set PY=.venv\Scripts\python.exe
) else (
  set PY=py -3
)
%PY% -m pytest -q --alluredir=allure-results %*
if errorlevel 1 (
  echo.
  echo ==== ESTI PALE ====
  echo skrinshoty v papke shots\
  exit /b 1
)
echo.
echo ==== VSE PROSHLO ====
echo rezultaty allure: allure-results
exit /b 0
