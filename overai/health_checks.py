"""
health_checks.py
Health and crash-loop protection for OverAI Windows overlay app.
Ported from the macOS version; log directory changed to %APPDATA%/overai/.
"""

import os
import sys
import time
import platform
import traceback
import functools
from pathlib import Path


def get_log_dir():
    """Return a persistent log directory under %APPDATA%/overai/."""
    appdata = os.environ.get("APPDATA", str(Path.home()))
    log_dir = Path(appdata) / "overai"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


LOG_DIR = get_log_dir()
LOG_PATH = LOG_DIR / "overai_error_log.txt"
CRASH_COUNTER_FILE = LOG_DIR / "overai_crash_counter.txt"
CRASH_THRESHOLD = 3
CRASH_TIME_WINDOW = 60


def get_system_info():
    """Return a string with Windows version, Python version, etc."""
    win_ver = platform.platform()
    python_version = platform.python_version()
    info = (
        "\n"
        "System Information:\n"
        f"  Windows: {win_ver}\n"
        f"  Python:  {python_version}\n"
    )
    return info


def check_crash_loop():
    """Read and update the crash counter; exit if a crash loop is detected."""
    current_time = time.time()
    count = 0
    last_time = 0

    if os.path.exists(CRASH_COUNTER_FILE):
        try:
            with open(CRASH_COUNTER_FILE, "r") as f:
                line = f.read().strip()
                if line:
                    last_time_str, count_str = line.split(",")
                    last_time = float(last_time_str)
                    count = int(count_str)
        except Exception:
            count = 0

    if current_time - last_time < CRASH_TIME_WINDOW:
        count += 1
    else:
        count = 1

    try:
        with open(CRASH_COUNTER_FILE, "w") as f:
            f.write(f"{current_time},{count}")
    except Exception as e:
        print("Warning: Could not update crash counter file:", e)

    if count > CRASH_THRESHOLD:
        print(
            f"ERROR: Crash loop detected (>{CRASH_THRESHOLD} crashes within "
            f"{CRASH_TIME_WINDOW}s).\n"
            f"Crash counter: {CRASH_COUNTER_FILE}\n"
            f"Error log:     {LOG_PATH}\n\n"
            f"Delete the counter file to retry:\n"
            f"  del \"{CRASH_COUNTER_FILE}\""
        )
        sys.exit(1)


def reset_crash_counter():
    """Reset the crash counter after a successful run."""
    if os.path.exists(CRASH_COUNTER_FILE):
        try:
            os.remove(CRASH_COUNTER_FILE)
        except Exception as e:
            print("Warning: Could not reset crash counter file:", e)


def health_check_decorator(func):
    """Wrap main() with crash-loop detection and error logging."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        check_crash_loop()
        try:
            result = func(*args, **kwargs)
            reset_crash_counter()
            return result
        except Exception:
            system_info = get_system_info()
            error_trace = traceback.format_exc()
            with open(LOG_PATH, "w") as log_file:
                log_file.write("An unhandled exception occurred:\n")
                log_file.write(system_info)
                log_file.write(error_trace)
            print("ERROR: Application failed to start properly. Details:")
            print(system_info)
            print(error_trace)
            print(f"Error log saved at: {LOG_PATH}", flush=True)
            sys.exit(1)
    return wrapper
