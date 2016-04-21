from __future__ import absolute_import
from celery.utils.log import get_task_logger
from umuco.models import *
from celery.decorators import  task
import datetime
from umuco.utils import flag_report


logger = get_task_logger(__name__)


@task(name="remind after 1 day")
def one_day_reminder():
    logger.info("Start task")
    today= datetime.datetime.today().weekday() + 1
    groups = NawenuzeGroup.objects.filter(day_of_meeting=today-1)
    for g in groups:
        if not g.report_set.filter(date_updated=datetime.date.fromordinal(datetime.date.today().toordinal()-1)):
            for tel in g.phonemodel_set.all():
                flag_report(tel.number, "Tu n as pas donne de rapport hier. Il faut l envoyer.")
                logger.info("Sent reminder to group {0} on {1}!".format(g, tel))


@task(name="remind after 2 day")
def two_days_reminder():
    day_of_week = datetime.datetime.today().weekday() + 1
    week = datetime.datetime.today().isocalendar()[1]
    groups = NawenuzeGroup.objects.filter(day_of_meeting=day_of_week)
    print groups, day_of_week, week
    logger.info("Sending reminder groups {0} , {1}, {2}!".format(groups, day_of_week, week))