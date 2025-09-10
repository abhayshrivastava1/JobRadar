import subprocess
import os
import webbrowser
import time
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Python backend folder
SCRAPPING_PATH = os.path.join(BASE_DIR, "scrapping backend")

# Node backend folder
BACKEND_PATH = os.path.join(BASE_DIR, "local backend")

FRONTEND_PATH = os.path.join(BASE_DIR, "frontend")  # better os.path.join

def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0

def wait_for_port(host, ports, label):
    print(f"⏳ Waiting for {label} to start...")
    while True:
        for port in ports:
            if is_port_open(host, port):
                print(f"✅ {label} is running on port {port}")
                return port
        time.sleep(1)

def run_all():
    try:
        # 1️⃣ Python backend
        # print("🚀 Starting Python backend (main.py)...")
        # subprocess.run(["python", "main.py"], cwd=SCRAPPING_PATH, check=True)

        # 2️⃣ Node server
        print("🌐 Starting Node server (main.js)...")
        subprocess.run(["node", "main.js"], cwd=BACKEND_PATH, check=True)

        # Wait for Node port
        node_port = wait_for_port("localhost", [5000], "Node server")

        # 3️⃣ Frontend
        print("💻 Starting frontend (npm run dev)...")
        subprocess.run(["npm", "run", "dev"], cwd=FRONTEND_PATH, shell=True, check=True)

        # Wait for frontend port
        frontend_port = wait_for_port("localhost", [5173, 5174, 5175, 5176], "Frontend")

        url = f"http://localhost:{frontend_port}"
        print(f"🌍 Opening browser at {url}")
        webbrowser.open(url)

    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while running: {e.cmd}")
        print("Exit code:", e.returncode)

if __name__ == "__main__":
    run_all()
