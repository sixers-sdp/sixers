import time
import traceback
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Net import *
import Phidget22
import threading

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

class WeightSensor:
    def __init__(self):
        self.weight_value = -1
        self.has_ended = False
        self.try_weight_sensor()

    def try_weight_sensor(self):
        print("Try Weight Sensor")
        try:
            # Allocate a new Phidget Channel object
            self.ch = VoltageRatioInput()
            self.do = DigitalOutput()

            self.ch.setChannel(0)
            self.do.setChannel(6)

            self.ch.setOnAttachHandler(onAttachHandler)
            self.ch.setOnDetachHandler(onDetachHandler)
            self.ch.setOnErrorHandler(onErrorHandler)
            self.ch.setOnVoltageRatioChangeHandler(onVoltageRatioChangeHandler)
            self.ch.setOnSensorChangeHandler(onSensorChangeHandler)
            # Open the channel with a timeout
            try:
                self.ch.openWaitForAttachment(5000)
                self.do.openWaitForAttachment(5000)
            except PhidgetException as e:
                # PrintOpenErrorMessage(e, self.ch)
                raise EndProgramSignal("Program Terminated: Open Failed")

            print("THREAD STARTING")

            weight_thread = threading.Thread(target=self.start_getting_weight_value)
            weight_thread.daemon = True
            weight_thread.start()

        except Exception as e:
            self.ch.close()
            self.try_conneting_again()

    def start_getting_weight_value(self):
        while not self.has_ended:
            try:
                self.weight_value = self.ch.getVoltageRatio()
            except:
                self.ch.close()
                break
            time.sleep(0.25)
        self.try_conneting_again()

    def try_conneting_again(self):
        self.has_ended = True
        print("Weight sensor failed! Trying to connect to the weight sensor again in 3 2 1...")
        time.sleep(3)
        self.ch = None
        self.do = None
        self.has_ended = False
        self.weight_value = -1
        self.try_weight_sensor()

    def get_weight_value(self):
        return self.weight_value
