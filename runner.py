import subprocess
import os
import time
import socket
import signal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCRAPPING_PATH = os.path.join(BASE_DIR, "scrapping backend")
BACKEND_PATH = os.path.join(BASE_DIR, "local backend")
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend")


def is_port_open(host, port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex((host, port)) == 0


def wait_for_port(host, ports, label):

    print(f"Waiting for {label} to start...")
    while True:
        for port in ports:
            if is_port_open(host, port):
                print(f"{label} is running on port {port}")
                return port
        time.sleep(1)

def run_all():
    processes = []
    try:

        print("Starting Python backend")
        py_proc = subprocess.Popen(
            ["python", "main.py"], cwd=SCRAPPING_PATH,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        processes.append(py_proc)
        py_proc.wait()  # Wait until Python backend finishes


        print("Starting Node server")
        node_proc = subprocess.Popen(
            ["node", "main.js"], cwd=BACKEND_PATH,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        processes.append(node_proc)

        # Wait until Node server is running
        wait_for_port("localhost", [5000], "Node server")


        print("Starting frontend")
        front_proc = subprocess.Popen(
            ["npm", "run", "dev"], cwd=FRONTEND_PATH,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        processes.append(front_proc)

        # Wait until frontend port is available
        wait_for_port("localhost", [5173, 5174, 5175, 5176], "Frontend")


        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        for proc in processes:
            proc.send_signal(signal.CTRL_BREAK_EVENT)
            proc.wait()
        print("All processes terminated")

    except Exception as e:
        print(f"Error: {e}")
        for proc in processes:
            proc.kill()

if __name__ == "__main__":
    run_all()
