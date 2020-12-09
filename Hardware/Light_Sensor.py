from grovepi import analogRead

from Hardware.Port_Settings import lightSensor

# sets the sensitivity of the light sensor to control readings. General resistance reading of dark overcast day is
# roughly 1.5K ohms resistance set higher to ensure capture from sunrise to sunset on those days as well.  Setting
# resistances too much higher than 1.5K ohms could begin to skew results from clear days by recording too early.
# For comparison full moonlight night on clear nights is roughly 70K ohms.
resistanceThreshold = 2000

# sets a defined resistance value to avoid division by zero in resistance calculation
MAX_RESISTANCE = 999999999


def obtainLightSensorValue():
    # obtains calculated resistance value of the light sensor to determine data collection.
    try:
        lightSensorValue = analogRead(lightSensor)

        # prevents a division by zero if lightSensorValue is 0 during darkness and thus crashing the program
        if lightSensorValue != 0:
            # calculates ohms of resistance based off light sensor readings
            resistance = float(1023 - lightSensorValue) * 10 / lightSensorValue

            return resistance

        else:
            resistance = MAX_RESISTANCE
            return resistance

    except IOError:
        print("Error -- obtainLightSensorValue")
