#!/usr/bin/env python3
import subprocess, time, argparse

def adb(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True)

def apply(profile):
    print(f"[{time.strftime("%H:%M")}] Profile: {profile}")
    if profile == "home":
        adb("settings put global data_roaming 0")
    else:
        adb("settings put global data_roaming 1")

if __name__ == "__main__":
    print("Roaming daemon active")
    while True:
        apply("roaming")
        time.sleep(60)
