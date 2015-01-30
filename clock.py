from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'clowder_product.settings'

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print ("is this working?")
    send_mail('Subject here', 'Is the clock working?.', 'admin@clowder.io',
    ['keith@parkme.com'], fail_silently=False)

sched.start()
