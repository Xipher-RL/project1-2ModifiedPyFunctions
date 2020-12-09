from grovepi import digitalWrite

from Hardware.Port_Settings import greenLED, blueLED, redLED


# applies the current weather status to the prescribed LED lighting nomenclature
def ledLightStatus(temperature, humidity):
    # 1 sends HIGH command to set LEDs to ON position
    if humidity > 80:
        digitalWrite(greenLED, 1)
        digitalWrite(blueLED, 1)

    else:
        if 60 < temperature < 85:
            digitalWrite(greenLED, 1)

        elif 85 < temperature < 95:
            digitalWrite(blueLED, 1)

        elif temperature > 95:
            digitalWrite(redLED, 1)

        # default statement to conditions not listed.
        else:
            ledLightsOff()


def ledLightsOff():
    # 0 sends LOW command to set LEDs to OFF position
    digitalWrite(greenLED, 0)
    digitalWrite(blueLED, 0)
    digitalWrite(redLED, 0)