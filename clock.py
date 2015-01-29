from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=3)
def timed_job():
    send_mail('Subject here', 'Is the clock working?.', 'admin@clowder.io',
    ['keith@parkme.com'], fail_silently=False)

sched.start()
