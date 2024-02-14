import serial

PORT = "COM4"
BAUD_RATE = 921600

with serial.Serial(PORT, BAUD_RATE, timeout=1) as ser:
    while True:
        try:
            value = ser.readline()
            print(value)
            data = [value.decode("ascii")]
        except Exception as e:
            print(
                e,
            )
            print("read value", value)
            continue

        print(data)
