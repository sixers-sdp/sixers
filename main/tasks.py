import time

import settings
import requests

from vision.exceptions import IncorrectNode
from vision.server import Server


class Task:
    """
    Abstract class for task handlers
    """

    # actions like move are better to be executed all at once instead of considering them separately
    # group_by = False

    success = False
    execute_all_at_once = False

    server = None

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
            if self.success:
                self.post_all_tasks()
            return

        for task in self.arguments_grouped:
            self.execute_one(task['args'])
            if self.success:
                self.post_task(task['args'])


class MoveTask(Task):
    """
    This just simulates moving
    """
    execute_all_at_once = True

    def post_new_location(self, location):
        r = requests.post(
            settings.API_LOCATION,
            data={'location': location.lower()},
            headers=settings.AUTH_HEADERS
        )
        r.raise_for_status()

    def post_all_tasks(self):
        self.post_new_location(self.arguments_grouped[-1]['args']['destination'])

    def execute_all(self):
        directions = [f['relative_direction'] for f in self.arguments_grouped]
        directions.append('END')
        directions.pop(0)

        nodes_expected = [f['args']['destination'] for f in self.arguments_grouped]
        # skip the first code
        print('QR codes expected:', nodes_expected)
        print('Directions')


        # is green:
        # if currently at table: its blue
        # if at chefs: we look for green

        is_green = self.arguments_grouped[0]['args']['origin'].lower() == 'chef'

        assert isinstance(self.server, Server), "Did you forgot to set up Server instance?"
        try:
            self.server.setup_order(directions, is_green, nodes_expected)
        except IncorrectNode as e:
            self.post_new_location(e.node_seen.lower())
            self.success = False
        self.success = True


class PickupTask(Task):
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

    def execute_one(self, task):
        time.sleep(10)
        self.success = True


class HandoverTask(Task):
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

    def execute_one(self, task):
        time.sleep(10)
        self.success = True
