# Wi-Fi Deauthentication Attack Detection

Real-time detection of Wi-Fi deauthentication attacks using an ESP32 microcontroller. Implements two detection methods (threshold and z-score) and tests them against a real Pwnagotchi attacker.

## How It Works

The ESP32 listens in promiscuous mode on a Wi-Fi channel and counts deauthentication/disassociation frames in 5-second windows. Two detection engines run simultaneously:

- **Threshold:** alerts if 10+ deauth frames arrive in one window
- **Z-score:** alerts if the count is statistically anomalous compared to a rolling baseline

## Hardware

- ESP32-WROOM-32D (detector)
- Raspberry Pi Zero 2 W running Pwnagotchi (attacker)
- Any Wi-Fi router as target AP

## Setup

1. Open `esp32/deauth_detector/deauth_detector.ino` in Arduino IDE
2. Change `#define CHANNEL` to match your router's channel
3. Upload to ESP32
4. Open Serial Monitor at 115200 baud

## Output

CSV over serial every 5 seconds:
```
timestamp_ms,window_deauths,total_deauths,threshold_alert,zscore,zscore_alert
```

## Data

The `data/` folder contains experiment captures from testing against Pwnagotchi and controlled attacks at various rates.

## License

MIT
