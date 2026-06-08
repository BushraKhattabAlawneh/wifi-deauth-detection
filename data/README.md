# Experiment Data

CSV files captured from the ESP32 detector during experiments.

| File | Description |
|------|-------------|
| `esp32_T1_pwnagotchi.csv` | Pwnagotchi attack (before baseline fix) |
| `esp32_T1_pwnagotchi_fixed.csv` | Pwnagotchi attack (after baseline fix) |
| `esp32_T2_flood.csv` | aireplay-ng continuous flood |
| `esp32_T3_evasion_sweep.csv` | Slow attack + evasion sweep (20 to 0.5 fps) |
| `esp32_T4_T5_no_attack.csv` | No attack, quiet + busy network |
| `esp32_full_session.csv` | Full session (attack + quiet combined) |

All CSVs have the format:
```
timestamp_ms,window_deauths,total_deauths,threshold_alert,zscore,zscore_alert
```
