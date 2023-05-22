import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Pandora I.A",
    version="1.5",
    description="Assistente virtual",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
