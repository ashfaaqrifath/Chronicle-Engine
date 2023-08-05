import datetime
import os
import sys
import time
import psutil
import logging
import colorama
import pygetwindow as gw
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

def progress(percent=0, width=30):
    symbol = width * percent // 100
    blanks = width - symbol
    print('\r[ ', Fore.GREEN + symbol * "█", blanks*' ', ' ]',
          f' {percent:.0f}%', sep='', end='', flush=True)

print()
print(Fore.BLACK + Back.YELLOW + " CHRONICLE ENGINE - ACTIVITY LOGGER ")
print("")
for i in range(101):
    progress(i)
    time.sleep(0.01)

print()
print(Fore.GREEN + "            Activated")
print()
print(Fore.LIGHTBLACK_EX + "Developed Ashfaaq Rifath - Chronicle Engine v1.2.1")
print()

date = datetime.datetime.now().strftime(f"%h{'('}%d{')'}:%H:%M")
log_file = str(date).replace(":", "-") + "-Log.txt"
folder = "Activity Logs"
save_log_file = os.path.join(folder, log_file)

logging.basicConfig(filename=save_log_file, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

logged_windows = set()

def open_program(app_name, app_path):
    try:
        os.startfile(app_path)
        logging.info(f"Opened {app_name}")
    except Exception as e:
        logging.error("ERROR")

def opened_windows():
    try:
        global logged_windows
        open_windows = gw.getWindowsWithTitle("")
        for window in open_windows:
            if window.title not in logged_windows:
                logging.info(f"Opened {window.title}")
                logged_windows.add(window.title)

        for title in logged_windows.copy():
            if title not in gw.getAllTitles():
                logging.info(f"Closed {title}")
                logged_windows.remove(title)
    except:
        print(Fore.RED + "Error Handled")

def main():
    time_stamp = datetime.datetime.now().strftime("%D:%h:%H:%M:%S")
    logging.info("CHRONICLE ENGINE v1.2.1\n" +
           str(time_stamp) + " \n<< ACTIVITY LOG >> \nBEGIN LOG >>\n")

    while True:
        opened_windows()

if __name__ == "__main__":
    main()