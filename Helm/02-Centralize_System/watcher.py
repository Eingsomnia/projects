import os
import time
import yaml
import requests
import fnmatch
import sys
import datetime
import threading
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

sys.stdout.reconfigure(line_buffering=True)

CONFIG_PATH = "/etc/file-watcher/config.yaml"
ALLOWED_EXTENSIONS = [".csv", ".xml", ".txt"]
SENT_CACHE_DIR = "/tmp/.sent-cache"

# Load config
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f) or {}

# Ensure sent cache dir exists
os.makedirs(SENT_CACHE_DIR, exist_ok=True)

def is_allowed_file(path):
    return any(path.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

def get_sent_marker_path(path):
    """Generate marker path for a file in writable /tmp"""
    filename = os.path.basename(path)
    return os.path.join(SENT_CACHE_DIR, f"{filename}.sent")

def has_been_sent(path):
    return os.path.exists(get_sent_marker_path(path))

def mark_as_sent(path):
    open(get_sent_marker_path(path), "w").close()

def send_file(path, endpoint):
    try:
        with open(path, 'rb') as f:
            raw_content = f.read()

        headers = {
            "Content-Type": "application/octet-stream",
            "X-Filename": os.path.basename(path)
        }

        for attempt in range(3):
            try:
                response = requests.post(endpoint, data=raw_content, headers=headers, timeout=10)
                if response.status_code == 200:
                    print(f"{datetime.datetime.now()} : [✔] Uploaded raw {path} to {endpoint}")
                    return True
                else:
                    print(f"{datetime.datetime.now()} : [✘] Upload failed ({response.status_code}) for {path}")
            except Exception as e:
                print(f"{datetime.datetime.now()} : [!] Attempt {attempt+1} error sending {path}: {str(e)}")
                time.sleep(2 ** attempt)  # backoff: 1s, 2s, 4s

    except Exception as e:
        print(f"{datetime.datetime.now()} : [!] Error reading file {path}: {str(e)}")
    return False

def match_file_rule(file_path, watch_config):
    filename = os.path.basename(file_path).lower()
    for watch in watch_config:
        for file_rule in watch.get("files", []):
            pattern = file_rule.get("pattern") or file_rule.get("Pattern")
            if pattern and fnmatch.fnmatch(filename, pattern.lower()):
                return file_rule.get("endpoint")
    return None

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_config):
        self.watch_config = watch_config
        self.timers = {}

    def on_any_event(self, event):
        print(f"{datetime.datetime.now()} : [DEBUG] Event: {event.event_type.upper()} → {event.src_path}")

    def on_modified(self, event):
        if event.is_directory or not is_allowed_file(event.src_path):
            return

        path = os.path.abspath(event.src_path)
        if path in self.timers:
            self.timers[path].cancel()

        t = threading.Timer(10.0, self.handle_stable_file, [path])
        self.timers[path] = t
        t.start()

    def handle_stable_file(self, path):
        if has_been_sent(path):
            print(f"{datetime.datetime.now()} : [~] Skipping already-sent file: {path}")
            return

        endpoint = match_file_rule(path, self.watch_config)
        if endpoint:
            print(f"{datetime.datetime.now()} : [✔] Stable file matched: {path} → {endpoint}")
            success = send_file(path, endpoint)
            if success:
                mark_as_sent(path)
        else:
            print(f"{datetime.datetime.now()} : [~] File ignored (no pattern match): {path}")

    def on_created(self, event):
        if event.is_directory or not is_allowed_file(event.src_path):
            return

        path = os.path.abspath(event.src_path)
        print(f"{datetime.datetime.now()} : [📄] New file created: {path}")

        if has_been_sent(path):
            print(f"{datetime.datetime.now()} : [~] Already sent (on create): {path}")
            return

        endpoint = match_file_rule(path, self.watch_config)
        if endpoint:
            print(f"{datetime.datetime.now()} : [+] New file matched: {path} → {endpoint}")
            success = send_file(path, endpoint)
            if success:
                mark_as_sent(path)

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileChangeHandler(config.get("watch_paths", []))

    for watch in config.get("watch_paths", []):
        path = watch.get("path")
        if not path:
            print(f"[⚠️] Skipping watch config (missing path): {watch}")
            continue
        print(f"{datetime.datetime.now()} : [~] Watching: {path}")
        observer.schedule(event_handler, path, recursive=True)

    observer.start()
    print(f"{datetime.datetime.now()} : 🚀 File watcher is running with PollingObserver...")

    try:
        while True:
            print(f"{datetime.datetime.now()} : ⏱️ Tick... still running")
            time.sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()