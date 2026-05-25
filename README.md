# Wi-Fi Deauthentication Attack Detection on Low-Cost Hardware

A comparative evaluation of Wi-Fi deauthentication detection approaches on constrained hardware (ESP32 and Raspberry Pi), tested against real automated attackers under varying attack intensities.

## Paper

**Title:** Real-Time Detection of Wi-Fi Deauthentication Attacks on Low-Cost Hardware: A Comparative Evaluation  
**Course:** CS11711 Data Communications and Networking, Spring 2026  
**Format:** IEEE conference style (LaTeX)

## Hardware Setup

| Device | Role |
|--------|------|
| RPi Zero W v1 | Attacker (Pwnagotchi) |
| RPi Zero W v2 | Detector — Python/Scapy |
| ESP32-WROOM-32D | Detector — C/Arduino |
| AirPort Extreme | Target AP |
| Phone/Laptop | Victim client |

## Detection Approaches

1. **Threshold** — frame count per sliding window
2. **Statistical (z-score)** — rolling baseline with anomaly detection
3. **Feature-based ML** — (future work)

## Repository Structure

```
esp32/           — ESP32 Arduino detector code
rpi/             — Raspberry Pi Python detector code
data/            — Experiment CSV results
scripts/         — Analysis and plotting scripts
paper/           — LaTeX source (or link to Overleaf)
docs/            — Notes, topology diagrams, etc.
```

## Test Matrix

| Test | Attack | Intensity | Measures |
|------|--------|-----------|----------|
| T1 | Pwnagotchi (auto) | High | Detection rate, latency |
| T2 | aireplay-ng --deauth 5 | Medium | Detection rate, latency |
| T3 | aireplay-ng --deauth 1 (slow) | Low | Evasion boundary |
| T4 | No attack | None | False positive rate |
| T5 | Busy network, no attack | None | FP under load |

## Future Work

- Adaptive threshold tuning via reinforcement learning
- Feature-based ML detector (decision tree / random forest)
- Multi-channel scanning
- Cross-platform resource usage comparison

## License

MIT
