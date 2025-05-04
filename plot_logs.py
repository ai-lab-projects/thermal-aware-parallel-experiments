# plot_logs.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
import matplotlib.dates as mdates

def plot_logs(log_dir="logs"):
    csv_files = glob.glob(os.path.join(log_dir, "log_*.csv"))
    if not csv_files:
        print(f"No log files found in {log_dir}.")
        return

    plt.figure(figsize=(14, 6))
    color_map = plt.get_cmap("tab10")
    marker_map = {"active": "o", "paused": "x"}

    for idx, csv_file in enumerate(sorted(csv_files)):
        df = pd.read_csv(csv_file)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", errors="coerce")
        df["status"] = df["throttling"].map(lambda x: "paused" if x else "active")

        label = os.path.basename(csv_file).replace("log_", "").replace(".csv", "")
        color = color_map(idx % 10)

        for status in ["active", "paused"]:
            sub_df = df[df["status"] == status]
            if not sub_df.empty:
                plt.scatter(
                    sub_df["timestamp"],
                    sub_df["temperature"],
                    label=f"{label} ({status})" if status == "active" else None,
                    marker=marker_map[status],
                    color=color,
                    s=50 if status == "paused" else 25,
                    alpha=0.8,
                )

    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title(f"CPU Temperature and Throttling - {log_dir}")
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
    plt.show()

# Optional direct call
if __name__ == "__main__":
    plot_logs()
