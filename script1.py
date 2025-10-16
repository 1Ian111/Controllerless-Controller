#script for the rasberry pi 
# shibu oli
# 2025-04-14
# This script runs on Raspberry Pi and sends 'a' over Wi-Fi every 3 seconds to the computer

import socket
import time

HOST = '10.61.134.158'  # computer's IP address
PORT = 65432            # Must match the port used on the computer

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        print(f"[+] Connected to {HOST}:{PORT}")
        
        while True:
            s.sendall(b'a')  # Send byte for 'a'
            print("Sent: a")
            time.sleep(3)    # Wait 3 seconds
            
    except ConnectionRefusedError:
        print("[!] Connection refused. Is the server running on the computer?")
    except Exception as e:
        print(f"[!] Error: {e}")
