# CPU Load and Thermal Throttling Analysis Framework

This project is a Python-based system for running CPU stress experiments under varying levels of parallelism, monitoring CPU temperatures using OpenHardwareMonitor, and analyzing thermal throttling and performance.

## Features

- Run CPU load experiments with configurable numbers of parallel worker processes
- Monitor CPU temperature in real time using OpenHardwareMonitor
- Automatically stop computations if temperature stays high too long (extra safety layer)
- Evaluate optimal number of worker processes by comparing computation counts
- Optional pause-on-overheat mode for thermal control (disabled by default)

## Requirements

- Python 3.x
- OpenHardwareMonitor v0.9.6 or compatible  
  Must be located at  
  ``openhardwaremonitor-v0.9.6/OpenHardwareMonitor/OpenHardwareMonitor.exe``
- Python packages:
  - ``numpy``
  - ``pandas``
  - ``matplotlib``
  - ``psutil``
  - ``requests``

Install dependencies with:

``pip install numpy pandas matplotlib psutil requests``

## Usage

### Run Experiments

To execute stress tests with different numbers of worker processes:

``python experiment_runner.py``

This runs tests with multiple process counts (e.g., 1, 2, 4, ..., 16).  
Each test logs CPU temperature and computation counts in a separate folder (e.g., ``logs_nproc_08``).  
There is a 60-second cooldown between each run to allow the system to recover.

The number of completed matrix multiplications is counted to help evaluate the performance impact of thermal throttling and guide selection of an optimal number of processes.

### Analyze Results

Open the notebook to compare results across experiments:

``compare_experiments.ipynb``

This notebook provides:

- Time-series plots of CPU temperature
- Visualization of throttling events
- Comparison of computation count and throttling frequency
- Analysis of optimal parallelism under thermal limits

## Temperature Safety

To protect the system from overheating, the framework includes the following:

- **Force-stop mechanism:**  
  If the temperature exceeds a threshold (default: ``85.0°C``) for more than ``30 seconds``, all computations are stopped.  
  This adds software-level safety even if the CPU has built-in thermal throttling or emergency shutdown.

- **Optional pause-on-overheat:**  
  The system includes a feature to temporarily pause computations instead of stopping them.  
  However, this is disabled by default (``enable_sleep=False``), as modern CPUs usually throttle automatically.

You can adjust the threshold with an environment variable:

``TEMP_THRESHOLD=90.0 python experiment_runner.py``

## Log Format

Each worker process generates a log file ``log_{proc_id}.csv`` with:

- ``timestamp``: ISO8601 time of measurement
- ``temperature``: Measured CPU temperature in Celsius
- ``throttling``: ``True`` if the program paused due to high temperature; otherwise ``False``
- ``count``: Number of matrix multiplication iterations completed

**Note:** ``throttling`` in this context refers to the application-level pause mechanism, not hardware thermal throttling.

## Notes

- OpenHardwareMonitor must be allowed to run with administrator privileges.
- The program polls temperature every ``0.1 seconds``, but OpenHardwareMonitor updates roughly every second.  
  For finer-grained thermal monitoring, alternative methods would be required.
- Workload consists of repeated matrix multiplications using NumPy to generate realistic CPU load.

## License

This project is licensed under the MIT License.
