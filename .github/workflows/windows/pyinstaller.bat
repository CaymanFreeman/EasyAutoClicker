@echo off
pyinstaller --noconfirm --onefile --name "EasyAutoClicker" --windowed --add-data="LICENSE.md;." --icon="assets\icon.ico" --add-data="assets\icon.png;assets" src\main.py