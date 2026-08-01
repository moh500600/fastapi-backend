@echo off
title Pharmacy Backend Server
cd /d E:\ph\my_app\backend

echo Starting backend...
python -m uvicorn api:app --reload

pause