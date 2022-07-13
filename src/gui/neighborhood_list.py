import serial as sr

# Write the AT command to QuectelEG25-G that list local celluar towers
with sr.Serial(port="/dev/ttyUSB3", baudrate=9600, timeout=3) as ser:
