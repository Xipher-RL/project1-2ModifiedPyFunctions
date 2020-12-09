from datetime import datetime

from grovepi import *

from FileControl.JSON_Report import appendWeatherData, weatherData, totalFileLocation, writeToJSONFile, pathName, \
    extensionType
from FileControl.Report_Control import nightlyUpload, weeklyMaintenance, failedDirectoryMaintenance, \
    uploadedDirectoryMaintenance
from FileControl.MongoDB import mongoDBListBuilder, mongoDBUploaderSystem, stringYesterDate
from Hardware.LED_Control import ledLightStatus, ledLightsOff
from Hardware.Light_Sensor import obtainLightSensorValue, resistanceThreshold
from Hardware.Temperature_Humidity_Sensor import Weather

while True:
    try:
        resistance = obtainLightSensorValue()

        # collect system time
        systemTime = datetime.now()
        stringTime = systemTime.strftime("%H:%M")

        # conditional to control readings taken during daylight hours.
        if resistance < resistanceThreshold:

            # creates weather data object from constructor
            WeatherData = Weather()

            # conversion from Celsius to Fahrenheit.
            WeatherData.temperatureConversion()

            # displays measurements if they were available from the sensor
            WeatherData.displayWeatherInfo()

            # adjusts weather station's external LED indicators lights to prescribed nomenclature
            ledLightStatus(WeatherData.temperature, WeatherData.humidity)

            # data collection and storage to JSON file
            appendWeatherData(stringTime, WeatherData.temperature, WeatherData.humidity)
            writeToJSONFile(totalFileLocation, weatherData)

            # sampling frequency of once every 30minutes(total) during daylight of weather data
            time.sleep(1790.0)

            # turns weather station's external LED indicators lights off shortly before taking a new sample
            ledLightsOff()

            # remainder of sleep timer to complete the 30minute total
            time.sleep(10.0)
        else:
            # turns weather station's external LED indicator lights off
            ledLightsOff()

            # displays calculated resistance to a connected monitor
            print("Outside Daylight parameters for data collection. Sensor Resistance = %.2f" % resistance)

            # performs methods to check to see if it is time to upload to MongoDB and to perform weekly maintenance
            uploadTime = nightlyUpload(systemTime)
            if uploadTime is True:
                mongoDBListBuilder(pathName, stringYesterDate, extensionType)
                mongoDBUploaderSystem(pathName, stringYesterDate)

                weeklyTime = weeklyMaintenance(systemTime)
                if weeklyTime is True:
                    failedDirectoryMaintenance()
                    uploadedDirectoryMaintenance()

                # checks to see if it is the correct day of the week to perform weekly file maintenance
                weeklyTime = weeklyMaintenance(systemTime)
                if weeklyTime is True:
                    failedDirectoryMaintenance()
                    uploadedDirectoryMaintenance()

            # Sampling frequency of once every 10minutes of brightness to resume weather data collection
            time.sleep(600.0)

    except KeyboardInterrupt:
        ledLightsOff()
        break
