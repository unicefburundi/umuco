from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger
from umuco.models import *
import datetime

logger = get_task_logger(__name__)


# @task(name="send_feedback_email_task")
# def send_feedback_email_task(email, message):
#     """sends an email when feedback form is filled successfully"""
#     logger.info("Sent feedback email")
#     return send_feedback_email(email, message)

@periodic_task(run_every=(crontab(minute='*/15')), name="remind to send", ignore_result=True)
def remind_to_send_reports():
    day_of_week = atetime.datetime.today().weekday()
    week = datetime.datetime.today().isocalendar()[1]
    groups = NawenuzeGroup.object.filter(day_of_gathering=day_of_week)

    logger.info("Sending reminder!")
