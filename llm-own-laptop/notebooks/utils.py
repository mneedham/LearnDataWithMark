import socket
import os 
import subprocess

def check_connectivity():
    ip_address = socket.gethostbyname(socket.gethostname())    
    if ip_address == "127.0.0.1":
        return f"No Network Connectivity (IP Address: {ip_address})"
    else:
        return f"You have Network Connectivity (IP Address: {ip_address})"


def toggle_wifi(value="off"):
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    try:
        subprocess.call(f"networksetup -setairportpower en0 {value}", shell=True)
        print("WiFi disabled.")
    except Exception as e:
        print(f"Failed to disable WiFi: {str(e)}")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
