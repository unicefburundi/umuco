from __future__ import absolute_import
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from umuco.models import *
from celery.decorators import periodic_task
import datetime


logger = get_task_logger(__name__)


# @task(name="send_feedback_email_task")
# def send_feedback_email_task(email, message):
#     """sends an email when feedback form is filled successfully"""
#     logger.info("Sent feedback email")
#     return send_feedback_email(email, message)

@periodic_task(run_every=(crontab(minute='*/1')), name="remind to send", ignore_result=False)
def remind_to_send_reports():
    day_of_week = datetime.datetime.today().weekday() + 1
    week = datetime.datetime.today().isocalendar()[1]
    groups = NawenuzeGroup.objects.filter(day_of_meeting=day_of_week)
    print groups, day_of_week, week
    logger.info("Sending reminder groups {0} , {1}, {2}!".format(groups, day_of_week, week))



from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
