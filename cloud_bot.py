# cloud_bot.py
from scanner import *
import time

print("🚀 Swing Bot Cloud Running...")

while True:
    try:
        print("Scanning stocks...")
        # run scanner
        exec(open("scanner.py").read())
        print("Scan completed. Sleeping 1 hour...")
        time.sleep(3600)  # run every 1 hour

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
