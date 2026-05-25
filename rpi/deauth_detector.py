#!/usr/bin/env python3
"""Wi-Fi Deauthentication Detector for Raspberry Pi (monitor mode)."""

import time
import math
import csv
import sys
from scapy.all import sniff, Dot11, Dot11Deauth, Dot11Disas

# --- Configuration ---
CHANNEL = 3
INTERFACE = "wlan1mon"
WINDOW_SEC = 5
THRESHOLD = 10
ZSCORE_THRESHOLD = 3.0
BASELINE_WINDOWS = 12

# --- State ---
window_count = 0
total_deauths = 0
history = []
window_start = time.time()
writer = None


def calc_zscore(count):
    n = len(history)
    if n < 3:
        return 0.0
    m = sum(history) / n
    sd = math.sqrt(sum((x - m) ** 2 for x in history) / n)
    if sd == 0:
        return 0.0
    return (count - m) / sd


def check_window():
    global window_count, window_start
    now = time.time()
    if now - window_start < WINDOW_SEC:
        return

    thresh_alert = 1 if window_count >= THRESHOLD else 0
    z = calc_zscore(window_count)
    z_alert = 1 if z > ZSCORE_THRESHOLD else 0

    row = [int((now - start_time) * 1000), window_count, total_deauths,
           thresh_alert, f"{z:.2f}", z_alert]
    writer.writerow(row)
    print(",".join(str(x) for x in row))

    # Update baseline
    history.append(window_count)
    if len(history) > BASELINE_WINDOWS:
        history.pop(0)

    window_count = 0
    window_start = now


def packet_handler(pkt):
    global window_count, total_deauths
    if pkt.haslayer(Dot11Deauth) or pkt.haslayer(Dot11Disas):
        window_count += 1
        total_deauths += 1
    check_window()


if __name__ == "__main__":
    start_time = time.time()
    output_file = sys.argv[1] if len(sys.argv) > 1 else "output.csv"

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp_ms", "window_deauths", "total_deauths",
                         "threshold_alert", "zscore", "zscore_alert"])
        print(f"RPi Deauth Detector started on {INTERFACE} channel {CHANNEL}")
        print("timestamp_ms,window_deauths,total_deauths,threshold_alert,zscore,zscore_alert")

        try:
            sniff(iface=INTERFACE, prn=packet_handler, store=0)
        except KeyboardInterrupt:
            print(f"\nStopped. Total deauths: {total_deauths}")
