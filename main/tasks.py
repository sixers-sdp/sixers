import settings
import requests


class Task:
    """
    Abstract class for task handlers
    """

    # actions like move are better to be executed all at once instead of considering them separately
    # group_by = False

    success = False
    execute_all_at_once = False

    def __init__(self, arguments_grouped):
        self.arguments_grouped = arguments_grouped

    def post_task(self, task):
        """
        Update API state here
        """
        pass


    def post_all_tasks(self):
        """
        Update API state here
        """
        pass

    def execute_one(self, task):
        pass

    def execute_all(self):
        pass

    def run(self):
        if self.execute_all_at_once:
            self.execute_all()
            self.post_all_tasks()
            return

        for task in self.arguments_grouped:
            self.execute_one(task['args'])
            self.post_task(task['args'])

class AbstractMoveTask(Task):
    """
    This just simulates moving
    """
    execute_all_at_once = True

    def post_all_tasks(self):
        r = requests.post(
            settings.API_LOCATION,
            data={'location': self.arguments_grouped[-1]['destination']},
            headers=settings.AUTH_HEADERS
        )
        r.raise_for_status()
        self.success = True


class AbstractPickupTask(Task):
    def post_task(self, task):
        # needs to update order state
        order_id = task['order'].strip('ORDER')
        url = settings.API_DETAIL_ORDER_URL.format(order_id)
        r = requests.patch(
            url,
            data={'state': 'delivery'},
            headers=settings.AUTH_HEADERS
        )
        print(r.content)
        r.raise_for_status()
        self.success = True


class AbstractHandoverTask(Task):
    def post_task(self, task):
        # needs to update order state
        order_id = task['delivery'].strip('ORDER')
        url = settings.API_DETAIL_ORDER_URL.format(order_id)
        r = requests.patch(
            url,
            data={'state': 'finished'},
            headers=settings.AUTH_HEADERS
        )
        r.raise_for_status()
        self.success = True


class MoveTask(AbstractMoveTask):
    pass

class PickupTask(AbstractPickupTask):
    pass

class HandoverTask(AbstractHandoverTask):
    pass
