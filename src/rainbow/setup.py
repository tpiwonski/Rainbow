from cx_Freeze import Executable, setup

exe = [Executable("main.py", targetName="rainbow")]

setup(
    name="rainbow",
    version="1.0",
    options={
        "build_exe": {
            "packages": ["os", "re", "click"],
            "include_files": []
        }
    },
    executables=exe)
