from grovepi import *


# grovePi board Port connections for hardware devices
# analog connections
lightSensor = 0

# digital connections
greenLED = 2
blueLED = 3
redLED = 4
temperature_humidity_sensor = 8

# sets the Light Sensor port as input.
pinMode(lightSensor, "INPUT")
pinMode(greenLED, "OUTPUT")
pinMode(blueLED, "OUTPUT")
pinMode(redLED, "OUTPUT")

# specific manufacture's code to identify the type of temperature/humidity sensor (0=blue, 1=white)
sensorTypeCode = 0



