from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.mail import send_mail

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=5)
def timed_job():
    send_mail('Subject here', 'Here is the message.', 'admin@clowder.io',
    ['keith@parkme.com'], fail_silently=False)

sched.start()
