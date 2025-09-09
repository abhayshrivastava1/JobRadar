import subprocess
import os
import webbrowser
import time
import platform
import socket

# Base directory = runner.py ka folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Relative paths
SCRAPPING_PATH = os.path.join(BASE_DIR, "scrapping backend")
BACKEND_PATH   = os.path.join(BASE_DIR, "local backend")
FRONTEND_PATH  = os.path.join(BASE_DIR, "frontend")

# Helper: check if port is open
def is_port_open(host, port):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

def run_all():
    try:
        # # 1. Run Python scrapping backend (main.py)
        # print("🚀 Starting Python backend (main.py)")
        # subprocess.run(["python", "main.py"], cwd=SCRAPPING_PATH, check=True)

       