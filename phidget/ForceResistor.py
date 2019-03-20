import time
import traceback
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Net import *

try:
    from PhidgetHelperFunctions import *
except ImportError:
    sys.stderr.write(
        "\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
        "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

lastVoltage = 0

def onAttachHandler(self):
    ph = self
    try:

        # Get device information and display it.
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if (ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Channel:  " + str(channel) + "\n")

        ph.setDataInterval(1000)
        ph.setVoltageRatioChangeTrigger(0.0)

        if (ph.getChannelSubclass() == ChannelSubclass.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT):
            ph.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_VOLTAGERATIO)


    except PhidgetException as e:
        DisplayError(e)
        traceback.print_exc()
        return


def onDetachHandler(self):
    ph = self

    try:

        # Get device information and display it.
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if (ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                  "\n\t-> Channel:  " + str(channel) + "\n")

    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return


def onErrorHandler(self, errorCode, errorString):
    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")


def onVoltageRatioChangeHandler(self, voltageRatio):
    global lastVoltage
    lastVoltage = voltageRatio
    print("[VoltageRatio Event] -> Voltage Ratio: " + str(voltageRatio))


def onSensorChangeHandler(self, sensorValue, sensorUnit):
    print("[Sensor Event] -> Sensor Value: " + str(sensorValue) + sensorUnit.symbol)


def main():
    try:
        # Allocate a new Phidget Channel object
        ch = VoltageRatioInput()
        do = DigitalOutput()

        ch.setChannel(0)
        do.setChannel(6)

        ch.setOnAttachHandler(onAttachHandler)
        ch.setOnDetachHandler(onDetachHandler)
        ch.setOnErrorHandler(onErrorHandler)
        ch.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)
        ch.setOnSensorChangeHandler(onSensorChangeHandler)

        # Open the channel with a timeout
        try:
            ch.openWaitForAttachment(5000)
            do.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch)
            raise EndProgramSignal("Program Terminated: Open Failed")

        # True should be replaced by while "moving" => currently requires manual stop
        while True:
            currentVoltageRatio = ch.getVoltageRatio()

            # If noticable change in Voltage occurs set off alarm
            if abs(currentVoltageRatio - lastVoltage) > 0.15:
                do.setState(True)
                time.sleep(0.5)
                do.setState(False)

        # Currently unreachable
        ch.close()
        return 0

    except PhidgetException as e:
        DisplayError(e)
        traceback.print_exc()
        ch.close()
        return 1
    except EndProgramSignal as e:
        print(e)
        ch.close()
        return 1
    except RuntimeError as e:
        traceback.print_exc()
        return 1
    finally:
        readin = sys.stdin.readline()


main()
