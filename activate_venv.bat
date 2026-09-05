@echo off
REM Script untuk aktivasi virtual environment di CMD
REM Gunakan: activate_venv.bat

call venv\Scripts\activate.bat
echo Virtual environment berhasil diaktifkan!
python --version

