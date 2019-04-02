import os
import time
import requests
import logging
import settings
import tasks
import sys

from api.map.east_right import convert_plan_to_relative_orientation
from utils import group_plan

sys.path.append(os.path.abspath('..'))

from vision.server import Server


TASKS = {
    'MOVE': tasks.MoveTask,
    'PICKUP': tasks.PickupTask,
    'HANDOVER': tasks.HandoverTask
}

GROUP_TASKS = ['MOVE']


class MainControl:
    """
    This is the main controller for all the other modules.
    It does following:

    - grabs plan from the server API
    - executes the plan one step at a time
    - for each step of the plan it will invoke appropriate function and give it full control.
    - the control resumes if the tasks succeeds or fails.
    - after it finishes executing the plan it will start polling the server for new plan.
    """

    current_plan = None

    def __init__(self):
        self.server = Server()

    def get_plan(self):
        r = requests.get(settings.API_CURRENT_PLAN_URL)
        r.raise_for_status()

        if r.status_code == 204:
            return

        self.current_plan = convert_plan_to_relative_orientation(r.json())
        self.plan_grouped = group_plan(self.current_plan)

        logging.info('Fetched a plan')

    def update_plan(self, data):
        r = requests.patch(
            settings.API_DETAIL_PLAN_URL.format(self.current_plan['id']),
            data=data,
            headers=settings.AUTH_HEADERS
        )
        r.raise_for_status()

    def loop(self):
        while True:
            if not self.current_plan:
                logging.info('Retrieving plan')
                self.get_plan()

            if not self.current_plan:
                logging.info('Waiting for a plan')
                time.sleep(1)
            else:
                self.execute_plan()


    def execute_group(self, action, group_data):
        task_class = TASKS[action]
        task = task_class(group_data)
        task.server = self.server

        task.run()
        return task

    def execute_plan(self):
        succeeded = True
        for group in self.plan_grouped:
            action = group[0]['action']
            task = self.execute_group(action, group)
            last_id = group[-1]['sub_id']
            logging.info('Executing {0}'.format(action))
            if task.success:
                self.report_success(last_id)
            else:
                self.report_failure(last_id)
                succeeded = False
                break
        if self.current_plan:
            new_state = 'finished' if succeeded else 'aborted'
            self.update_plan({'state': new_state})
            self.current_plan = None


    def report_success(self, sub_id):
        logging.info('Task {0} succeeded.'.format(sub_id))
        self.update_plan({'steps_executed': sub_id})

    def report_failure(self, sub_id):
        logging.error('Task {0} failed.'.format(sub_id))

        self.update_plan({
            'steps_executed': sub_id,
            'state': 'aborted'
        })
        self.current_plan = None



if __name__ == '__main__':
    logging.info("Starting control loop")
    MainControl().loop()
