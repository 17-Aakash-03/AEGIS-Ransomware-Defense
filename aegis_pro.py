import time
import psutil
import win32gui
import win32process
import os
import hashlib
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# PASTE YOUR KEY INSIDE THE QUOTES BELOW
API_KEY = 'YOUR_API_KEY_HERE'
MONITOR_DIR = os.path.join(os.getcwd(), "TestZone")

# PEELER THRESHOLD: Ransomware writes faster than humans (approx 0.15s)
SPEED_THRESHOLD = 0.15

class AegisPro(FileSystemEventHandler):
    def __init__(self):
        self.last_access = {}
        self.process_cache = {}

    def get_file_hash(self, filepath):
        """Layer 1: Calculate SHA256 hash for Static Analysis."""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except:
            return None

    def check_virustotal(self, file_hash):
        """Layer 1: Query VirusTotal API for known signatures."""
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {"x-apikey": API_KEY}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                stats = response.json()['data']['attributes']['last_analysis_stats']
                return stats['malicious']
        except:
            return None
        return 0

    def analyze_process_context(self, pid):
        """Identify the actor and perform Hybrid Analysis."""
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name()
            proc_path = proc.exe()
        except:
            return "Unknown", 0

        # Check cache first to save API calls
        if pid in self.process_cache:
            return proc_name, self.process_cache[pid]

        print(f"\n[SCANNING] New Process Detected: {proc_name}")
       
        # --- LAYER 1: API CHECK ---
        file_hash = self.get_file_hash(proc_path)
        threat_score = 0
        if file_hash:
            threat_score = self.check_virustotal(file_hash)
            if threat_score is not None:
                print(f"   \_ VirusTotal Detection: {threat_score}/70 vendors")
                self.process_cache[pid] = threat_score
       
        return proc_name, (threat_score if threat_score else 0)

    def on_modified(self, event):
        if event.is_directory: return

        filename = os.path.basename(event.src_path)
        current_time = time.time()
       
        # --- LAYER 2: BEHAVIORAL SPEED CHECK ---
        last_time = self.last_access.get(filename, 0)
        time_diff = current_time - last_time
        self.last_access[filename] = current_time
       
        if last_time == 0: return

        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            is_visible = win32gui.IsWindowVisible(hwnd)
        except:
            return

        proc_name, api_threat_score = self.analyze_process_context(pid)

        # --- DECISION ENGINE ---
        if api_threat_score > 3:
            print(f"\n[!!!] BLOCKED (Signature): {proc_name} is known MALWARE.")
            print(f"      \_ Action: Process Killed (Simulated)")

        elif time_diff < SPEED_THRESHOLD:
            print(f"\n[!!!] BLOCKED (Behavior): {proc_name} is modifying files too fast ({time_diff:.4f}s).")
            print(f"      \_ Indicator: Rapid I/O Pattern")
       
        elif is_visible:
            print(f"[OK] Human Activity: {filename}")

if __name__ == "__main__":
    if not os.path.exists(MONITOR_DIR): os.makedirs(MONITOR_DIR)
    print("--- AEGIS PRO: HYBRID DEFENSE ACTIVE ---")
    observer = Observer()
    observer.schedule(AegisPro(), MONITOR_DIR, recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()