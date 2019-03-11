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


    def update_plan(self, data):
        r = requests.put(
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

            self.execute_plan()

    def execute_task(self, task_data):
        task_class = self.tasks_handlers[task_data['action']]
        task = task_class(task_data['args'])
        task.run()
        return task

    def execute_plan(self):
        for step in self.current_plan['steps']:
            time.sleep(1)

            logging.info(f'Executing {step}')
            task = self.execute_task(step)
            if task.success:
                self.report_success(step['sub_id'])
            else:
                self.report_failure(step['sub_id'])
                break

        self.update_plan({'state': 'finished'})
        self.current_plan = None


    def report_success(self, sub_id):
        logging.info(f'Task {sub_id} succeeded.')

        self.update_plan({'steps_executed': sub_id})

    def report_failure(self, sub_id):
        logging.error(f'Task {sub_id} failed.')

        self.update_plan({
            'steps_executed': sub_id,
            'state': 'aborted'
        })
        self.current_plan = None


if __name__ == '__main__':
    logging.info("Starting control loop")
    MainControl().loop()
