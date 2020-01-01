# Sonorus
A Harry Potter themed, illuminated bluetooth speaker. A nerdy gift, for a nerdy friend.

## Setup
More information to come later.

### Raspberry Pi
Bluetooth & bluealsa setup guide:
https://gist.github.com/mill1000/74c7473ee3b4a5b13f6325e9994ff84c

Tweak service to set Bluetooth capabilities
`sudo nano /lib/systemd/system/bluealsa.service`
```
ExecStart=/usr/bin/bluealsa -p a2dp-sink
```

Reload the service

`sudo systemctl daemon-reload`

`sudo systemctl restart bluealsa.service`

Set Bluetooth to allow pinless pairing
`sudo hciconfig hci0 sspmode 1`

### NeoPixel Setup

`sudo apt-get install python3-pip`

`sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`

### Sonorus Service
TODO: Add service & asound config.

## Notes & Learnings

Mixing NeoPixels with the Raspberry Pi's onboard 3.5mm audio jack is a pain since they both rely on overlapping PWM. I ended up using a USB audio adapter, at the cost of needing to cram things into my enclosure with very little spare room.
