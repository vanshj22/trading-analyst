@echo off
cd api
echo Starting Backend on Port 8001...
uvicorn main:app --reload --port 8001
pause
