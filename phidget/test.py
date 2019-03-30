from ForceResistor import WeightSensor
import time

sensor = WeightSensor()
while True:
    print(sensor.get_weight_value())
    time.sleep(1)
