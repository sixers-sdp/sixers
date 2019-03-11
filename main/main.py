import time
import requests
import logging
import settings
from tasks import DumbMoveTask, DumbPickupTask, DumbHandoverTask


TASKS_DEBUG = {
    'MOVE': DumbMoveTask,
    'PICKUP': DumbPickupTask,
    'HANDOVER': DumbHandoverTask
}

TASKS_REAL = {}

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

    if settings.DEBUG:
        tasks_handlers = TASKS_DEBUG
    else:
        tasks_handlers = TASKS_REAL

    def get_plan(self):
        plan_r = requests.get(settings.API_CURRENT_PLAN_URL)
        plan_r.raise_for_status()
        self.current_plan = plan_r.json()
        logging.info('Fetched a plan')

    def loop(self):
        while True:
            if not self.current_plan:
                self.get_plan()

            if not self.current_plan:
                logging.info('Waiting for a plan')
                time.sleep(1)

            self.execute_plan()

    def execute_task(self, task):
        task_class = self.tasks_handlers[task['action']]
        task = task_class(task['args']).run()

        if task.success:
            self.report_success(task['sub_id'])
        else:
            self.report_failure(task(['sub_id']))

    def execute_plan(self):
        for step in self.current_plan['steps']:
            logging.info(f'Executing {step}')
            pass

    def report_success(self, sub_id):
        raise NotImplementedError

    def report_failure(self, sub_id):
        raise NotImplementedError


if __name__ == '__main__':
    logging.info("Starting control loop")
    MainControl().loop()


