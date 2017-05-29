from rpipms.plan_tower_observer import PlanTowerObserver


class ConsoleObserver(PlanTowerObserver):
    def notify(self, data):
        print(data)
