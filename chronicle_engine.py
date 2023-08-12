import datetime
import os
import sys
import time
import psutil
import win32com.client
import logging
import threading
import colorama
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
print(Fore.LIGHTBLACK_EX + " Copyright © Ashfaaq Rifath - Chronicle Engine v1.2.0")
print()

date = datetime.datetime.now().strftime(f"%h{'('}%d{')'}:%H:%M")
log_file = str(date).replace(":", "-") + "-Log.txt"
folder = "Activity Logs"
save_log_file = os.path.join(folder, log_file)

logging.basicConfig(filename=save_log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logged_windows = set()

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

                elif window.title == "H:/":
                    logging.info("Opened RACHINTER (H:)")

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

def key_release(key):
    if key == keyboard.Key.esc:
        return False

def log_keystrokes():
    time_stamp = datetime.datetime.now().strftime("%D:%h:%H:%M:%S")
    with open(save_log_file, "a") as f:
        f.write("CHRONICLE ENGINE v1.2.0\n" +
        str(time_stamp) + " \n<< KEYSTROKE LOG >> \n\n")
    
    with keyboard.Listener(on_press=key_press, on_release=key_release) as watcher:
        watcher.join()

def log_activity():
    time_stamp = datetime.datetime.now().strftime("%D:%h:%H:%M:%S")
    logging.info("CHRONICLE ENGINE v1.2.0\n" +
        str(time_stamp) + " \n<< ACTIVITY LOG >> \n")

    while True:
        log_windows()

if __name__ == "__main__":
    keystroke_thread = threading.Thread(target=log_keystrokes)
    activity_thread = threading.Thread(target=log_activity)

    keystroke_thread.start()
    activity_thread.start()

    keystroke_thread.join()
    activity_thread.join()
