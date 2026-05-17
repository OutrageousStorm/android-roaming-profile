#!/usr/bin/env python3
"""
auto_switch_daemon.py -- Automatically apply network profiles based on roaming state.
Runs in background and switches settings when roaming is detected.
Usage: python3 auto_switch_daemon.py --home-profile home.json --roaming-profile roaming.json
"""
import subprocess, json, time, argparse, sys
from pathlib import Path

def adb(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True)

def get_roaming_state():
    r = subprocess.run("adb shell dumpsys telephony.registry | grep mDataRoaming",
                      shell=True, capture_output=True, text=True)
    return 'true' in r.stdout.lower() or '1' in r.stdout

def apply_profile(profile_file):
    """Load JSON profile and apply settings via ADB"""
    with open(profile_file) as f:
        profile = json.load(f)
    
    for setting in profile.get('settings', []):
        namespace = setting.get('namespace', 'global')
        key = setting['key']
        value = setting['value']
        adb(f"settings put {namespace} {key} {value}")
    
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--home-profile', required=True, help='JSON profile for home network')
    parser.add_argument('--roaming-profile', required=True, help='JSON profile for roaming')
    parser.add_argument('--interval', type=int, default=60, help='Check interval')
    args = parser.parse_args()
    
    if not Path(args.home_profile).exists() or not Path(args.roaming_profile).exists():
        print("❌ Profile files not found")
        sys.exit(1)
    
    print("🚀 Auto-Switch Daemon — Ctrl+C to stop")
    prev_state = get_roaming_state()
    
    try:
        while True:
            time.sleep(args.interval)
            curr = get_roaming_state()
            if curr != prev_state:
                profile = args.roaming_profile if curr else args.home_profile
                apply_profile(profile)
                status = "ROAMING" if curr else "HOME"
                print(f"[{time.strftime('%H:%M:%S')}] Applied {status} profile")
                prev_state = curr
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == '__main__':
    main()
