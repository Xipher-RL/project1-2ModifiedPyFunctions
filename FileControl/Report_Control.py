import datetime
import os
import shutil

from FileControl.JSON_Report import pathName, extensionType



# Establish yesterday's date for JSON file name.
currentDate = datetime.date.today()
deltaDate = datetime.timedelta(1)
yesterdayDate = currentDate - deltaDate
stringYesterDate = yesterdayDate.strftime("%Y-%m-%d")

# path names for success and fails
successExtendPath = "Uploaded/"
failureExtendPath = "Failed_Upload/"
finalFailurePath = pathName + failureExtendPath + "Manual_Upload_Required/"
successTotalPath = pathName + successExtendPath
failureTotalPath = pathName + failureExtendPath


# moves files if upload to MongoDB succeeded
def uploadSuccess(fileLocation, fileName):
    if os.path.exists(pathName + successExtendPath) is False:
        print("File Control Error: Creating directory: " + successTotalPath)
        os.mkdir(successTotalPath)

    shutil.move(fileLocation + fileName + extensionType, successTotalPath + fileName + extensionType)


# moves files if upload to MongoDB failed
def uploadFailure(fileLocation, fileName):
    if os.path.exists(pathName + failureExtendPath) is False:
        print("File Control Error: Creating directory: " + failureTotalPath)
        os.mkdir(failureTotalPath)

    shutil.move(fileLocation + fileName + extensionType, failureTotalPath + fileName + extensionType)


def uploadFinalFailure(fileLocation, fileName):
    if os.path.exists(finalFailurePath) is False:
        print("File Control Error: Creating directory: " + finalFailurePath)
        os.mkdir(finalFailurePath)

    shutil.move(fileLocation + fileName + extensionType, finalFailurePath + fileName + extensionType)


# method to check if it is time to perform the nightly upload of the prior day's JSON file
def nightlyUpload(time):
    rangeLowDate = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=1, minute=1, second=00, microsecond=00))
    rangeHighDate = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=1, minute=11, second=00, microsecond=00))

    if rangeLowDate <= time < rangeHighDate:
        return True
    else:
        return False


def weeklyMaintenance(day):
    weeklyMaintenanceDate = "Sunday"

    if day.strftime("%A") == weeklyMaintenanceDate:
        return True
    else:
        return False


# weekly maintenance of Uploaded reports discarding those that are older than 7 days
def uploadedDirectoryMaintenance():
    daysOfKeptReports = 7

    i = 1
    while i <= daysOfKeptReports:
        maintenanceDeltaDate = datetime.timedelta(i + daysOfKeptReports)
        maintenanceDate = currentDate - maintenanceDeltaDate
        stringMaintenanceDate = maintenanceDate.strftime("%Y-%m-%d")
        maintenanceTotalPath = pathName + successExtendPath + stringMaintenanceDate + extensionType

        if os.path.isfile(maintenanceTotalPath) is True:
            os.remove(maintenanceTotalPath)

        i += 1


# weekly maintenance of Failed_Upload reports, with second attemp to up load reports and re-organizing based on status
def failedDirectoryMaintenance():
    failedDirectoryPath = pathName + failureExtendPath

    with os.scandir(failedDirectoryPath) as availableFiles:
        for file in availableFiles:
            if file.is_file() and extensionType in file.name:
                from FileControl.MongoDB import mongoDBListBuilder
                mongoDBListBuilder(failedDirectoryPath, file.name.split(".")[0], extensionType)
                from FileControl.MongoDB import mongoDBUploaderSystem
                mongoDBUploaderSystem(failedDirectoryPath, file.name.split(".")[0])
