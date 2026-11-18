@echo off
cd /d %~dp0
if not exist .venv (py -m venv .venv)
call .venv\Scripts\activate
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo .env fayliga BOT_TOKEN kiriting, so'ng qayta ishga tushiring.
pause
python main.py
