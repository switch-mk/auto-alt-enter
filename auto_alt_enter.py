import subprocess
import sys

try:
    import keyboard
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
    import keyboard

try:
    import win32gui
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    import win32gui

import argparse
import time
import ctypes
import os
from datetime import datetime


def find_antigravity_window():
    results = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "antigravity" in title.lower():
                results.append((hwnd, title))
        return True

    win32gui.EnumWindows(callback, None)
    return results


def activate_and_send(hwnd):
    # ALT押しっぱなし回避のため、先にリリース
    keyboard.release('alt')
    keyboard.release('enter')
    time.sleep(0.05)

    # ウィンドウをフォアグラウンドに
    ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.2)

    # ALT+ENTER送信
    keyboard.send('alt+enter')


def get_latest_commit(repo_path):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path, capture_output=True, text=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", "-i", type=float, default=3)
    parser.add_argument("--repo", "-r", type=str, default=None,
                        help="Git repo path to watch for commits. Stops after a new commit.")
    args = parser.parse_args()

    initial_commit = None
    if args.repo:
        repo = os.path.abspath(args.repo)
        initial_commit = get_latest_commit(repo)
        if initial_commit:
            print(f"=== ALT+ENTER auto sender ===")
            print(f"Interval: {args.interval}s")
            print(f"Watching: {repo}")
            print(f"Current commit: {initial_commit[:8]}")
            print(f"Will stop after new commit\n")
        else:
            print(f"Warning: Could not read git repo at {repo}")
            print(f"Running without commit detection\n")
            args.repo = None
    else:
        print(f"=== ALT+ENTER auto sender ===")
        print(f"Interval: {args.interval}s")
        print(f"Ctrl+C to stop\n")

    try:
        while True:
            # Check for new commit
            if args.repo and initial_commit:
                current = get_latest_commit(repo)
                if current and current != initial_commit:
                    now = datetime.now().strftime("%H:%M:%S")
                    print(f"\n[{now}] New commit detected: {current[:8]}")
                    print("Stopping.")
                    return

            windows = find_antigravity_window()
            now = datetime.now().strftime("%H:%M:%S")
            if not windows:
                print(f"[{now}] Waiting for Antigravity window...")
            else:
                for hwnd, title in windows:
                    activate_and_send(hwnd)
                    short = title[:60] + "..." if len(title) > 60 else title
                    print(f"[{now}] ALT+ENTER -> {short}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
