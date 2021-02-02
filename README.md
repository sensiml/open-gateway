# SensiML Simple Streaming Gateway

This Simple Streaming Gateway implements the Simple Streaming Service Wi-Fi protocol to enable forwarding data to the SensiML Data Capture Lab. The Simple Streaming Gateway supports connecting to sensors sources over a serial or BLE connection.

The Gateway must first be configured to record data from your target sensor. It does that by fetching a configuration file. You can scan for devices connected over serial and configure the Application by fetching the configuration from the connected device.

![Configure Gateway](img/configure.png)

After fetching the configuration your gateway is ready to stream out data. You can then use the SensiML Data Capture lab to connect and record live sensor data.

You can also use the Gateway to view the live sensor data streams

![View Sensor Data](img/stream.png)

As well as the results stream

![View Results](img/results.png)

## Installation

To install the app dependencies run

```bash
cd simple-streaming-gateway
pip install -r requirements.txt
```

To Start the application run

```bash
python3 app.py
```

## Data Collection over Serial Source

    1. Connect edge node to Gateway over USB serial
    2. Go to Gateway Configure Screen, Select Serial Radio and Click Scan
    3. Enter the Device ID (which is the port) into the Text Field and Click Configure
    4. The Simple Streaming Gateway is now configured to Stream Data from your Device over Wi-Fi

**NOTE** The BAUD RATE for the serial connection can be changed in the app.py by updating the default BAUD_RATE configuration.

## Data Collection over BLE Source

    1. Connect edge node to Gateway over USB serial
    2. Go to Gateway Configure Screen, Select BLE Radio and Click Scan
    3. Enter the Device ID (which is the port) into the Text Field and Click Configure
    4. The Simple Streaming Gateway is now configured to Stream Data from your Device over Wi-Fi

**NOTE** To use Bluethooth as a source you may have to run the following to allow bluepy-helper to access the correct permissions

## Data Collection from TCP/IP Source

    1. Connect edge node to network
    2. Go to Gateway Configure Screen, Select TCP/IP Radio Button
    3. Enter the Device ID (address:port) into the Text Field and Click Configure
    4. The Simple Streaming Gateway is now configured to Stream Data from your Device over Wi-Fi

**NOTE** To use Bluethooth as a source you may have to run the following to allow bluepy-helper to access the correct permissions

```bash
find ~/ -name bluepy-helper
cd <PATH>
sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper
```
