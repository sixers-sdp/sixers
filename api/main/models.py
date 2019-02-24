import os
import re
import subprocess

from django.db import models

from django.conf import settings
from django.template.loader import render_to_string

ORDER_STATE_NEW = 'new'
ORDER_STATE_DELIVERY = 'delivery'
ORDER_STATE_FINISHED = 'finished'
ORDER_STATE_ABORTED = 'aborted'

ORDER_STATE_CHOICES = [
    (s, s)
    for s in [ORDER_STATE_NEW, ORDER_STATE_DELIVERY, ORDER_STATE_FINISHED, ORDER_STATE_ABORTED]
]


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

    table_number = models.IntegerField()

    products = models.ManyToManyField(Product)
    state = models.CharField(
        default=ORDER_STATE_NEW,
        choices=ORDER_STATE_CHOICES,
        max_length=24
    )

    def __str__(self):
        return f"{self.state}: {self.updated_at}"


class ExecutionPlan(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    plan_out = models.TextField(null=True)
    plan_parsed = models.TextField(null=True)

    def __str__(self):
        return f'{self.created_at}'

    @classmethod
    def create_new(cls):
        """
        runs ff with following arguments:
        - domain file - static file
        - problem file - rendered template capturing the world right now
        """
        plan = cls()
        plan.save()

        # 1. generate problem file
        context = {}
        problem_content = render_to_string('problem.pddl', context)
        problem_file = os.path.join(settings.MEDIA_ROOT, f'problem_{plan.id}.pddl')

        with open(problem_file, 'w') as static_file:
            static_file.write(problem_content)

        # 2. locate domain file:
        domain_file = os.path.join(settings.BASE_DIR, '..', 'map', 'domain.pddl')
        assert os.path.exists(domain_file)

        # 3. run FF with the file arguments
        ff_out = subprocess.run(
            [settings.FF_EXECUTABLE, '-o', domain_file, '-f', problem_file],
            stdout=subprocess.PIPE
        )

        plan.plan_out = ff_out.stdout.decode("utf-8")

        plan_parsed = [
            line.strip().lstrip('step').strip()
            for line in plan.plan_out.splitlines()
            if re.match('(step)? \s+ \d+: .*', line)
        ]


        plan.plan_parsed = '\n'.join(plan_parsed)
        plan.save()

        return plan



