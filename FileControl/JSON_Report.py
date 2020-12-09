import datetime
import json
import os

# establish date for fileName
systemDate = datetime.date.today()
stringDate = systemDate.strftime("%Y-%m-%d")

# path, name and extension variables for location to store current weather data
pathName = "/home/pi/Reports/"
fileName = stringDate
extensionType = ".json"
totalFileLocation = pathName + fileName + extensionType

weatherData = []


def writeToJSONFile(location, data):
    if os.path.exists(pathName) is False:
        print("File Control Error: Creating directory: " + pathName)
        os.mkdir(pathName)

    with open(location, 'w', encoding='utf-8') as output:
        json.dump(data, output)


def appendWeatherData(time, temperature, humidity):
    weatherData.append([time, temperature, humidity])
