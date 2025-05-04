# experiment_utils.py
import os
import shutil
import subprocess
import psutil

def ensure_ohm_running():
    def is_ohm_running():
        for proc in psutil.process_iter(['name']):
            if "OpenHardwareMonitor.exe" in (proc.info.get('name') or ""):
                return True
        return False

    if not is_ohm_running():
        subprocess.run([
            'powershell', '-Command',
            'Start-Process "openhardwaremonitor-v0.9.6/OpenHardwareMonitor/OpenHardwareMonitor.exe" -Verb runAs'
        ])

def run_experiment(n_proc, log_dir_base="logs_nproc"):
    ensure_ohm_running()

    log_dir = f"{log_dir_base}_{n_proc:02d}"
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    processes = []
    for i in range(n_proc):
        proc_id = f"P{i+1}"
        print(f"[{proc_id}] Launching process")
        cmd = ["python", "worker_proc.py", proc_id, log_dir]
        p = subprocess.Popen(cmd)
        processes.append(p)

    for p in processes:
        p.wait()
