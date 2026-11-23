import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
APP_FILE = BASE_DIR / "app.py"

subprocess.run([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    str(APP_FILE)
])