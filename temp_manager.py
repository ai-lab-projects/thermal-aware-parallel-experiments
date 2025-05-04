# temp_manager.py
import os
import csv
import time
import requests
from datetime import datetime

TEMP_THRESHOLD = float(os.getenv("TEMP_THRESHOLD", 85.0))
INTERVAL_SEC = 0.1
TARGET_CORE_NUMS = [1, 2, 3, 4]
log_files = {}

# 高温がこの秒数以上続いたら強制停止する（例：3秒）
MAX_HIGH_TEMP_DURATION = 30.0

# プロセスごとの高温連続開始時刻
high_temp_start_times = {}

def get_metrics():
    try:
        response = requests.get("http://localhost:8085/data.json")
        data = response.json()
        temps = {}

        def find_nodes(node):
            if isinstance(node, dict):
                text = node.get("Text", "")
                value = node.get("Value", "")
                if "°C" in value:
                    try:
                        val = float(value.split(" ")[0])
                        if "CPU Core" in text or "CPU Package" in text:
                            temps[text] = val
                    except:
                        pass
                for child in node.get("Children", []):
                    find_nodes(child)

        find_nodes(data)
        return temps
    except:
        return {}

def control_temperature(proc_id, log_dir, count, enable_sleep=True):
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"log_{proc_id}.csv")

    if proc_id not in log_files:
        log_files[proc_id] = open(log_path, mode="w", newline="")
        writer = csv.writer(log_files[proc_id])
        writer.writerow(["timestamp", "temperature", "throttling", "count"])
        high_temp_start_times[proc_id] = None
    else:
        writer = csv.writer(log_files[proc_id])

    while True:
        temps = get_metrics()
        core_temps = [v for k, v in temps.items() if any(f"CPU Core #{n}" in k or "CPU Package" in k for n in TARGET_CORE_NUMS)]
        current_max = max(core_temps) if core_temps else 0
        now = datetime.now().isoformat(timespec='milliseconds')

        if current_max >= TEMP_THRESHOLD:
            writer.writerow([now, current_max, True, count])

            # 初回の高温なら時刻記録
            if high_temp_start_times[proc_id] is None:
                high_temp_start_times[proc_id] = time.time()
            else:
                elapsed = time.time() - high_temp_start_times[proc_id]
                if elapsed >= MAX_HIGH_TEMP_DURATION:
                    writer.writerow([now, current_max, "FORCED STOP", count])
                    raise RuntimeError("Temperature too high for too long. Aborting computation.")

            if enable_sleep:
                time.sleep(INTERVAL_SEC)
            else:
                break
        else:
            writer.writerow([now, current_max, False, count])
            high_temp_start_times[proc_id] = None
            break
