@echo off
title 💰 Finance Tracker — Starting...
color 0A
echo.
echo  ============================================
echo   💰 Finance Tracker — Starting up...
echo  ============================================
echo.
echo  Installing required packages...
pip install -r requirements.txt --quiet
echo.
echo  Launching your dashboard...
echo  Your browser will open automatically.
echo  (Keep this window open while using the app)
echo.
streamlit run app.py --server.headless false
pause
