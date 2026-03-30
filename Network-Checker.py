import subprocess
import socket
from datetime import datetime

def check_ping(ip):
    try:
        output = subprocess.check_output(f"ping -n 1 -w 500 {ip}", shell=True, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def check_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip, port))
    s.close()
    return result == 0

def network_scanner(network_prefix):
    print(f"\n--- Scan Started: {datetime.now()} ---")
    active_devices = 0
    failed_devices = 0
    
    # Range from 1 to 254
    for i in range(1, 255):
        target_ip = f"{network_prefix}.{i}"
        
        if check_ping(target_ip):
            print(f"[+] SUCCESS: Device {target_ip} is Online")
            active_devices += 1
            if not check_port(target_ip, 80):
                print(f"    [!] SERVICE ERROR: Port 80 (HTTP) down on {target_ip}")
        else:
            # This will show you exactly which IP is not responding
            print(f"[-] FAILED: Device {target_ip} is Offline/Unreachable")
            failed_devices += 1
        
    print(f"\n--- Scan Summary ---")
    print(f"Total Online: {active_devices}")
    print(f"Total Offline: {failed_devices}")

if __name__ == "__main__":
    user_input = input("Enter the network prefix (e.g., 192.168.1): ")
    network_scanner(user_input)