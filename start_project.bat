@echo off

:: Start the frontend
start cmd /c "cd f && npm run dev"

:: Start the backend
python backend\app.py
