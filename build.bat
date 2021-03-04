@echo off
pip install --upgrade pyinstaller
pyinstaller widget.py --onefile --windowed --add-data 'icon.png;.' --add-data 'Montserrat.ttf;.'
pyinstaller config.py --onefile --windowed
echo '' 
echo 'Done building. Files are in "dist" folder.'