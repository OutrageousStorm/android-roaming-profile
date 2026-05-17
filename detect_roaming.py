#!/usr/bin/env python3
"""
detect_roaming.py -- Detect when device switches to roaming and alert user.
Monitors ADB connection for roaming flag changes.
Usage: python3 detect_roaming.py --alert-command "notify-send 'Now roaming!'"
"""
import subprocess, time, argparse, sys

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_roaming_state():
    """Check if device is currently on roaming network"""
    # Check telephony service
    state = adb("dumpsys telephony.registry | grep mDataRoaming")
    return 'true' in state.lower() or '1' in state

def get_carrier():
    """Get current carrier name"""
    return adb("getprop gsm.nitz.time") or adb("getprop gsm.operator.iso-country") or "unknown"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', type=int, default=30, help='Check interval (seconds)')
    parser.add_argument('--alert-command', help='Command to run when roaming detected')
    args = parser.parse_args()

    print("📡 Roaming Detector — Ctrl+C to stop")
    prev_state = get_roaming_state()
    print(f"Initial state: {'🌍 ROAMING' if prev_state else '📶 HOME'}\n")

    try:
        while True:
            time.sleep(args.interval)
            curr = get_roaming_state()
            if curr != prev_state:
                carrier = get_carrier()
                if curr:
                    print(f"⚠️  SWITCHED TO ROAMING — {carrier}")
                    if args.alert_command:
                        subprocess.run(args.alert_command, shell=True)
                else:
                    print(f"✅ BACK TO HOME NETWORK — {carrier}")
                prev_state = curr
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == '__main__':
    main()
