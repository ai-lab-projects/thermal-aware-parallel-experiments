# worker_proc.py
import sys
import os
import time
import numpy as np
import temp_manager

# Fixed duration for this worker
duration_sec = 60

# Parse arguments
proc_id = sys.argv[1]
log_dir = sys.argv[2]

# Start computation
start_time = time.time()
count = 0

while time.time() - start_time < duration_sec:
    # Perform workload
    for _ in range(10):
        a = np.random.rand(1000, 1000)
        _ = np.dot(a, a)
        count += 1

    # Call temperature manager
    temp_manager.control_temperature(proc_id, log_dir, count, enable_sleep=False)


print(f"[{proc_id}] Finished - total iterations: {count}")
