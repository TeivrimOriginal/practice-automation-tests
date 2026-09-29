@echo off
setlocal
if exist .venv\Scripts\python.exe (
  set PY=.venv\Scripts\python.exe
) else (
  set PY=py -3
)
%PY% -m pytest -q --alluredir=allure-results %*
where allure >nul 2>nul
if errorlevel 1 (
  echo.
  echo allure CLI ne nayden. Postavye Allure Commandline ^(nuzhna Java^)
  echo ili zapustite: npx allure serve allure-results
  echo gotovye rezultaty lezhat v papke allure-results
  exit /b 0
)
allure generate allure-results -o allure-report --clean
allure open allure-report
