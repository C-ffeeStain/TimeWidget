import re
from version import Version
import urllib.request as request
from pathlib import Path
from subprocess import Popen

def self_update():
    with open("VERSION") as v:
        cur_version = Version(v.read())
    with request.urlopen("https://github.com/c-ffeestain/timewidget/raw/main/VERSION") as f:
        new_version = Version(f.read())
    if cur_version < new_version:
        print("Current version:", cur_version, "\n", "New version:", new_version)
        choice = input("Outdated version, would you like to download the newest one (Y/n)? ").lower()
        if choice == "y":
            cur_path = Path(__file__).parent
            wdt_exe = cur_path / "widget.exe"
            cfg_exe = cur_path / "config.exe"
            print("Backing up executables...")
            
            wdt_exe = wdt_exe.rename(wdt_exe.stem + ".backup" + wdt_exe.suffix)
            cfg_exe = cfg_exe.rename(cfg_exe.stem + ".backup" + cfg_exe.suffix)

            print("Executables backed up as {} and {}. Downloading new version now!".format(wdt_exe.name, cfg_exe.name))
            request.urlretrieve("https://github.com/c-ffeestain/timewidget/releases/latest/download/widget.exe","widget.exe")
            request.urlretrieve("https://github.com/c-ffeestain/timewidget/releases/latest/download/config.exe", "config.exe")

            print("Running new exe...")
            Popen([str(wdt_exe)])

if __name__ == "__main__":
    self_update()