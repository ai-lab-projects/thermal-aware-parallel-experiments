# experiment_runner.py
import time
from experiment_utils import run_experiment

# Settings
process_counts = [1, 2, 4, 6, 8, 10, 12, 16]
cooldown_duration = 60

print("==== Experiment Start ====")

for n_proc in process_counts:
    print(f"\n=== Running with {n_proc} processes ===")
    run_experiment(n_proc)
    print("==== Experiment Complete ====")
    print(f"\nCooling down for {cooldown_duration} seconds...\n")
    time.sleep(cooldown_duration)

print("==== All Experiments Complete ====")
