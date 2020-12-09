import math

import grovepi

from Hardware.Port_Settings import temperature_humidity_sensor, sensorTypeCode


# constructor for Weather objects and related functions
class Weather:
    SensorData = []

    def __init__(self):
        try:
            SensorData = grovepi.dht(temperature_humidity_sensor, sensorTypeCode)
            self.temperature = SensorData[0]
            self.humidity = SensorData[1]

        except IOError:
            print("Error -- Temp/Humidity Sensor")

    def temperatureConversion(self):
        # conversion from Celsius to Fahrenheit.
        self.temperature = ((self.temperature * 1.8) + 32)

    def displayWeatherInfo(self):
        # displays measurements if they were available from the sensor to connected monitor
        if math.isnan(self.temperature) == False and math.isnan(self.humidity) == False:
            print("temp = %.02f F humidity =%.02f%%" % (self.temperature, self.humidity))
