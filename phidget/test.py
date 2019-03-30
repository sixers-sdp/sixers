from ForceResistor import WeightSensor
import time

sensor = WeightSensor()
def run():
	for i in range(10):
	    print(sensor.get_weight_value())
	    time.sleep(1)

import threading
t = threading.Thread(target=run)
t.start()
