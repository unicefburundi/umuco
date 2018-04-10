from __future__ import absolute_import
from celery.utils.log import get_task_logger
from umuco.models import *
from celery.decorators import periodic_task
import datetime
from umuco.utils import flag_report


logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour=9, minute=30)), name="remind_after_1_day", ignore_result=False)
def one_day_reminder(days=1):
    logger.info("Start task")
    days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    groups = NawenuzeGroup.objects.filter(day_of_meeting=days_ago.weekday()+1)
    for g in groups:
        if not g.report_set.filter(date_updated=datetime.date.fromordinal(datetime.date.today().toordinal()-1)):
            for tel in g.phonemodel_set.all():
                flag_report(tel.number, "Tugire nawe nuze. Umugwi wanyu {0} ntiwatanze raporo ejo haheze. Tubasavye kuyirungika.".format(g))
                logger.info("Sent reminder to group {0} on {1}!".format(g, tel))


@periodic_task(run_every=(crontab(hour=9, minute=30)), name="remind_after_2_day", ignore_result=False)
def two_days_reminder(days=2):
    days_ago = datetime.datetime.now() - datetime.timedelta(days=days)
    groups = NawenuzeGroup.objects.filter(day_of_meeting=days_ago.weekday()+1)
    for g in groups:
        if not g.report_set.filter(date_updated=datetime.date.fromordinal(datetime.date.today().toordinal()-1)):
            for tel in g.phonemodel_set.all():
                flag_report(tel.number, "Tugire nawe nuze. Umugwi wanyu {0} umaze imisi ibiri udatanga raporo. Tubasavye kuyirungika canke mubibwire uwubakurikirana mwikomine.".format(g))
            for As in g.animateursocial_set.all():
                flag_report(As.telephone, "Tugire nawe nuze, {1}. Umugwi {0} umaze imisi ibiri udatanga raporo. Rungika ijambo NAWENUZE kuri 505 kugira utumenyeshe ingorane yoba ihari.".format(g, As))

                logger.info("Sending reminder to {0} on group {1}, for {2}!".format(As, g, days_ago))
