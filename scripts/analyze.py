#!/usr/bin/env python3
"""Analyze experiment CSV and print summary metrics."""

import csv
import sys


def analyze(filepath):
    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    total_windows = len(rows)
    attack_windows = [r for r in rows if int(r["window_deauths"]) > 0]
    thresh_alerts = sum(1 for r in rows if int(r["threshold_alert"]) == 1)
    zscore_alerts = sum(1 for r in rows if int(r["zscore_alert"]) == 1)
    total_deauths = int(rows[-1]["total_deauths"]) if rows else 0

    print(f"File: {filepath}")
    print(f"Total windows: {total_windows}")
    print(f"Windows with deauths: {len(attack_windows)}")
    print(f"Total deauth frames: {total_deauths}")
    print(f"Threshold alerts: {thresh_alerts}")
    print(f"Z-score alerts: {zscore_alerts}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <csv_file>")
        sys.exit(1)
    analyze(sys.argv[1])
