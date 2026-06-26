import json
import os
import sys
from pathlib import Path

def open_json(file_name):
    path = relative_path(file_name)
    with open(path, "r") as file:
        data = json.load(file)
    return data

def load_json(contents):
    return json.loads(contents)

def relative_path(file_name):
    if getattr(sys, "frozen", False):
        # Running as .exe
        folder = sys._MEIPASS
    else:
        # Running as .py
        folder = os.path.dirname(__file__)

    return os.path.join(folder, file_name)

def save_json(dir, file_name, data):
    path = Path(dir) / file_name
    with open(path, "w") as file:
        json.dump(data, file, indent=4)