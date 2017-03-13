# -*- coding: utf-8 -*-
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files": ['player.png']}

setup(  name = "CSCI-413-Project-Version-1.0",
        version = "1.0",
        description = "A maze-based game written in Python using Pygame.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Main.py", base=None)])