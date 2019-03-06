import time
import requests
import logging
from main import settings


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
    last_plan = None


    def get_plan(self):
        plan_r = requests.get(settings.API_CURRENT_PLAN_URL)
        plan_r.raise_for_status()
        self.current_plan = plan_r.json()
        logging.debug('Fetched a plan')


    def loop(self):
        while True:
            if not self.current_plan:
                self.get_plan()

            if not self.current_plan:
                time.sleep(1)

            self.execute_plan()

    def execute_plan(self):
        pass


