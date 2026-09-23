@echo off
cd /d "C:\Users\Gourav\loot_deals_bot"
:loop
"C:\Users\Gourav\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe" bot.py >> bot_output.log 2>&1
timeout /t 5 /nobreak >nul
goto loop
