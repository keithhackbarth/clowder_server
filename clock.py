from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'clowder_product.settings'

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    send_mail('Subject here', 'Is the clock working?.', 'admin@clowder.io',
    ['keith@parkme.com'], fail_silently=False)

sched.start()
