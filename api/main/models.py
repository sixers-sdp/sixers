import os
import re
import subprocess

from django.db import models

from django.conf import settings
from django.template.loader import render_to_string
from map import cafe_map


ORDER_STATE_NEW = 'new'
ORDER_STATE_READY = 'ready'
ORDER_STATE_DELIVERY = 'delivery'
ORDER_STATE_FINISHED = 'finished'
ORDER_STATE_ABORTED = 'aborted'

ORDER_STATE_CHOICES = [
    (s, s)
    for s in [ORDER_STATE_NEW, ORDER_STATE_READY, ORDER_STATE_DELIVERY, ORDER_STATE_FINISHED, ORDER_STATE_ABORTED]
]

PLAN_STATE_NEW = 'new'
PLAN_STATE_FINISHED = 'finished'
PLAN_STATE_ABORTED = 'aborted'

PLAN_STATE_CHOICES = [
    (s, s)
    for s in [PLAN_STATE_NEW, PLAN_STATE_FINISHED, PLAN_STATE_ABORTED]
]


class DotAssociation(models.Model):
    dot_id = models.CharField(max_length=248)
    location = models.CharField(max_length=20)


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    table_number = models.CharField(
        max_length=30,
        choices=[(t, t) for t in  cafe_map.tables]
    )

    products = models.ManyToManyField(Product, blank=True)
    products_text = models.TextField(null=True)

    state = models.CharField(
        default=ORDER_STATE_NEW,
        choices=ORDER_STATE_CHOICES,
        max_length=24
    )

    def __str__(self):
        return f"order{self.pk}"


class PDDLError(Exception):
    pass


class ExecutionPlan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    plan_parsed = models.TextField(null=True)
    steps_executed = models.IntegerField(null=True)

    state = models.CharField(
        default=PLAN_STATE_NEW,
        choices=PLAN_STATE_CHOICES,
        max_length=24
    )

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-id']

    def __str__(self):
        return f'{self.created_at}'

    @classmethod
    def create_new(cls):
        """
        runs ff with following arguments:
        - domain file - static file
        - problem file - rendered template capturing the world right now
        """

        # 1. generate problem file
        context = {
            'current_location': LocationUpdate.objects.latest(),
            'chef_location': cafe_map.CHEF,
            'ready_orders': Order.objects.filter(state=ORDER_STATE_READY),
            'delivery_orders': Order.objects.filter(state=ORDER_STATE_DELIVERY),
            'locations': cafe_map.current_map.nodes,
            'edges': cafe_map.adjacency,
        }

        # if there is nothing to be done do not generate new plan!
        actions_count = context['ready_orders'].count() + context['delivery_orders'].count()
        if not actions_count:
            return None

        plan = cls()
        plan.save()

        problem_content = render_to_string('problem.pddl', context)
        problem_file = os.path.join(settings.MEDIA_ROOT, f'problem_{plan.id}.pddl')

        with open(problem_file, 'w') as static_file:
            static_file.write(problem_content)

        # 2. locate domain file:
        domain_file = os.path.join(settings.BASE_DIR, 'map', 'domain.pddl')
        assert os.path.exists(domain_file)

        # 3. run FF with the file arguments
        ff_out = subprocess.run(
            [settings.FF_EXECUTABLE, '-o', domain_file, '-f', problem_file],
            stdout=subprocess.PIPE
        )

        # Solution is generated to the problem_xx.pddl.ff file
        solution_file = os.path.join(settings.MEDIA_ROOT, f'problem_{plan.id}.pddl.ff')
        if not os.path.exists(solution_file):
            raise PDDLError(ff_out.stdout.decode("utf-8"))


        with open(solution_file) as f:
            plan_plaintext = f.read()

        # 4. parse the actual lines of the plan
        plan_pattern = re.compile("\((?P<content>.*)\)")
        plan_parsed = [
            re.search(plan_pattern, line).group("content").strip()
            for line in plan_plaintext.splitlines()[1:]
            if re.match(plan_pattern, line)
        ]

        # 5. save the cleaned version of the plan to the database.
        plan.plan_parsed = '\n'.join(plan_parsed)
        plan.save()

        return plan

    def plan_as_json(self):
        """
        Parses the text file with plan and returns it as JSON representation
        """
        plan = []

        args_mapping = {
            'PICKUP': ['agent', 'order', 'location'],
            'HANDOVER': ['agent', 'location', 'delivery'],
            'MOVE': ['agent', 'destination', 'origin', 'direction']
        }

        if not self.plan_parsed:
            return []

        for counter, step in enumerate(self.plan_parsed.splitlines()):
            action, *args = step.split()

            mapping = args_mapping[action]
            plan.append({
                'sub_id': counter,
                'action': action,
                'args': dict(zip(mapping, args))
            })
        return plan


class LocationUpdate(models.Model):
    update = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=20)

    class Meta:
        ordering = ('-update',)
        get_latest_by = 'update'

    def __str__(self):
        return f'{self.location}'
