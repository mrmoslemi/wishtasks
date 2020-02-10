import string
import requests
from random import random
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from django.db import models


def generate_random_code():
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(127))


def run(task_id):
    def run_function():
        task = Task.objects.get(id=task_id)
        task.run()

    return run_function


class Task(models.Model):
    SCHEDULED = 'scheduled'
    SUSPENDED = 'suspended'
    EXECUTED = 'executed'
    MISSED = 'missed'
    STATE_CHOICES = (
        (SCHEDULED, 'Scheduled Task'),
        (SUSPENDED, 'Suspended Task'),
        (EXECUTED, 'Executed Task'),
        (MISSED, 'Missed Task'),
    )
    creation = models.DateTimeField(auto_now_add=True)
    execution = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=127, default=generate_random_code)
    state = models.CharField(max_length=9, choices=STATE_CHOICES, default=SCHEDULED)

    scheduled = models.DateTimeField()
    callback = models.URLField()

    def schedule(self):
        if self.execution > timezone.now():
            scheduler = BackgroundScheduler()
            scheduler.add_job(run(self.id), 'date', run_date=self.scheduled)
            scheduler.start()
        else:
            self.run()

    def run(self):
        if self.state == Task.SCHEDULED:
            data = {'code': self.code}
            result = requests.post(url=self.callback, data=data)
            if result.status_code == 200:
                self.executed()
            else:
                self.missed()

    def executed(self):
        self.execution = timezone.now()
        self.state = Task.EXECUTED
        self.save()

    def suspended(self):
        self.state = Task.SUSPENDED
        self.save()

    def missed(self):
        self.state = Task.MISSED
        self.save()

    def __str__(self):
        return self.code
