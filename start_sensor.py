import yaml
import os

from rpipms.plan_tower_sensor import PlanTowerSensor
# from rpipms.observers.oled_observer import OledObserver
from rpipms.observers.console_observer import ConsoleObserver

if __name__ == "__main__":
    try:
        # Load example config for PlanTower PMS7003
        with open(os.path.dirname(os.path.abspath(__file__)) + '/config.yml') as data_file:
            config = yaml.load(data_file)

        sensor = PlanTowerSensor()
        sensor.configure(config)  # override config with custom

        # PlanTower data observers
        sensor.add_observer(ConsoleObserver())
        # sensor.add_observer(OledObserver())

        sensor.start()  # start measure
    except KeyboardInterrupt:
        pass
