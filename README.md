# SensiML Simple Streaming Gateway

This application works as example application code for developing a gateway for emmbedded devices using the  SensiML Simple Streaming service.


To install the app dependencies run

```bash
cd fkask_simple_stream
pip install -r requirements.txt
```

1. Flash a data collection binary to your target IoT device.
2. Connect to the device over usb.
3. Start the application using
    python app.py
4. To configure the serial port for the app go to /serialport
5. To configure the app with the embedded devices configuration go to /config
6. To start streaming data go to /stream


TO USE BLUETOOTH YOU WILL NEED TO FIND BLUEPY HELPER

```bash
find ~/ -name bluepy-helper
cd <PATH>
sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper
```
