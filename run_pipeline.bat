@echo off
SET PIPELINE_DIR=c:\Users\raiak\OneDrive\Desktop\python\pipeline\job finder
cd /d "%PIPELINE_DIR%"
python pipeline.py
echo Pipeline executed at %date% %time% >> pipeline_log.txt
