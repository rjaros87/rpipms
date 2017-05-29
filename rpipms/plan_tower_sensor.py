import time
import traceback

from .plan_tower_device import PlanTowerDevice


class PlanTowerSensor:
    observers = []
    config = None

    def configure(self, configure):
        self.config = configure

    def add_observer(self, observer):
        self.observers += [observer]

    def notify_all(self, data):
        for observer in self.observers:
            try:
                observer.notify(data)
            except:
                print("Observer error: ")
                traceback.print_exc()

    def start(self):
        plan_tower = PlanTowerDevice(self.config)
        plan_tower.execute_command(PlanTowerDevice.MODE_WAKEUP)
        plan_tower.execute_command(PlanTowerDevice.MODE_ACTIVE)

        measurement_samples = self.config['no_samples']
        standby_time = self.config['standby_time']
        data_collection = []

        while True:
            data = plan_tower.read()
            if type(data) is dict or standby_time >= 45:
                data_collection.append(data)

                if len(data_collection) >= measurement_samples:
                    plan_tower.execute_command(PlanTowerDevice.MODE_SLEEP)
                    self.notify_all(self.analyze_measurement_data(data_collection))
                    data_collection = []  # clear collection
                    time.sleep(standby_time)
                    plan_tower.execute_command(PlanTowerDevice.MODE_WAKEUP)
                    plan_tower.execute_command(PlanTowerDevice.MODE_ACTIVE)
            else:
                self.notify_all(data)
                time.sleep(standby_time)

    def analyze_measurement_data(self, data_collection):
        # TODO: prepare analyze function for data collected form device
        return data_collection[-1]  # Temporary return last result
