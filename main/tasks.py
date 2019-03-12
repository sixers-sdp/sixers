import settings
import requests


class Task:
    """
    Abstract class for task handlers
    """

    # actions like move are better to be executed all at once instead of considering them separately
    # group_by = False

    success = False

    def __init__(self, arguments):
        self.arguments = arguments

    def post_task(self):
        """
        Update API state here
        """
        pass

    def pre_task(self):
        pass

    def execute(self):
        pass

    def run(self):
        self.pre_task()
        self.execute()
        self.post_task()


class AbstractMoveTask(Task):
    """
    This just simulates moving
    """

    def post_task(self):
        r = requests.post(
            settings.API_LOCATION,
            data={'location': self.arguments['destination']},
            headers=settings.AUTH_HEADERS
        )
        r.raise_for_status()

    def execute(self):
        self.success = True


class AbstractPickupTask(Task):
    def post_task(self):
        # needs to update order state
        order_id = self.arguments['order'].strip('ORDER')
        url = settings.API_DETAIL_ORDER_URL.format(order_id)
        r = requests.patch(
            url,
            data={'state': 'delivery'},
            headers=settings.AUTH_HEADERS
        )
        print(r.content)
        r.raise_for_status()

    def execute(self):
        self.success = True


class AbstractHandoverTask(Task):
    def post_task(self):
        # needs to update order state
        order_id = self.arguments['delivery'].strip('ORDER')
        url = settings.API_DETAIL_ORDER_URL.format(order_id)
        r = requests.patch(
            url,
            data={'state': 'finished'},
            headers=settings.AUTH_HEADERS
        )
        r.raise_for_status()

    def execute(self):
        self.success = True


class MoveTask(AbstractMoveTask):
    def execute(self):
        super(MoveTask, self).execute()


class PickupTask(AbstractPickupTask):
    def execute(self):
        super(PickupTask, self).execute()

class HandoverTask(AbstractHandoverTask):
    def execute(self):
        super(HandoverTask, self).execute()

