import datetime
import json
import os
from datetime import datetime as DT

import requests
from pymongo import MongoClient

from FileControl.JSON_Report import extensionType, pathName
from FileControl.Resource0 import getList
from FileControl.Report_Control import uploadSuccess, uploadFailure, uploadFinalFailure

# Establish yesterday's date for JSON file name.
currentDate = datetime.date.today()
deltaDate = datetime.timedelta(1)
yesterdayDate = currentDate - deltaDate
stringYesterDate = yesterdayDate.strftime("%Y-%m-%d")

jsonList = []


def mongoDBListBuilder(fileLocation, file, ext):
    # validates there is a file to open
    if os.path.isfile(fileLocation + file + ext) is True:
        # opens JSON file
        with open(fileLocation + file + ext, 'r') as f:
            fileData = json.load(f)

            # converts JSON of raw sensor data into appropriate list of MongoDB formatted dictionaries
        for item in fileData:
            jsonItem = {"time": None, "temperature": None, "humidity": None, 'time': item[0],
                            'temperature': item[1], 'humidity': item[2]}

        jsonList.append(jsonItem)


def mongoDBUploaderSystem(fileLocation, collectionName):
    # validates there is a file to open
    if os.path.isfile(fileLocation + collectionName + extensionType) is True:

        # pulls database list information
        myList = getList()

        # MongoDB Client method settings
        R0C = MongoClient("mongodb+srv://" + myList[0] + ":" + myList[1] + "@" + myList[2] +
                          ".mjmit.mongodb.net/" + myList[3] + "?retryWrites=true&w=majority")
        # MongoDB name
        R0DB = R0C[myList[3]]

        try:
            # MongoDB upload method selection based on input data structure type
            if isinstance(jsonList, list):
                R0DB[collectionName].insert_many(jsonList)

            else:
                R0DB[collectionName].insert_one(jsonList)

            reportAgeLimit = datetime.date.today() - datetime.timedelta(7)
            reportAgeLimit = DT.combine(reportAgeLimit, datetime.time(0, 0))

            # checks for collection present on MongoDB system and moves files accordingly
            if collectionName in R0DB.list_collection_names() and DT.strptime(collectionName, "%Y-%m-%d") > reportAgeLimit:
                # move file to uploaded
                uploadSuccess(fileLocation, collectionName)

            elif collectionName in R0DB.list_collection_names() and DT.strptime(collectionName, "%Y-%m-%d") < reportAgeLimit:
                # removes the reports if they are uploaded and older than 7 days
                os.remove(fileLocation + collectionName + extensionType)

            elif collectionName not in R0DB.list_collection_name() and fileLocation is pathName:
                # moves file to the Failed_Upload location to be retried later.
                uploadFailure(fileLocation, collectionName)

            else:
                # move file to location for manual upload
                uploadFinalFailure(fileLocation, collectionName)

        except requests.exceptions.RequestException as e:
            print(e)
