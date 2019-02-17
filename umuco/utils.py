import csv
import datetime
import json
import urllib

import requests

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models.query import QuerySet
from django.http import HttpResponse
from pytz import timezone

timezone("Africa/Bujumbura")


class ExcelResponse(HttpResponse):
    def __init__(
        self,
        data,
        output_name="Report_Muco",
        headers=None,
        force_csv=False,
        encoding="utf8",
        font="",
    ):
        valid_data = False
        if isinstance(data, QuerySet):
            data = list(data.values())
        elif hasattr(data, "__getitem__"):
            if isinstance(data[0], dict):
                if headers is None:
                    headers = data[0].keys()
                data = [[row[col] for col in headers] for row in data]
                data.insert(0, headers)
            if hasattr(data[0], "__getitem__"):
                valid_data = True
        else:
            data = list(data)
        assert valid_data is True, "ExcelResponse requires a sequence of sequences"

        import StringIO

        output = StringIO.StringIO()
        writer = csv.writer(output)
        writer.writerows(data)
        content_type = "text/csv"
        file_ext = "csv"
        output.seek(0)
        super(ExcelResponse, self).__init__(
            content=output.getvalue(), content_type=content_type
        )
        self["Content-Disposition"] = 'attachment;filename="%s.%s.%s"' % (
            output_name.replace('"', '"'),
            datetime.datetime.now().strftime("%d %b %Y  %p"),
            file_ext,
        )


def validate_date(date_text):
    try:
        date = datetime.datetime.strptime(date_text, "%d%m%y")
    except ValueError:
        raise ValueError("Date est incorecte. Le format est jjmmaa.")
    else:
        return date


def split_message(request):
    response_data = {}
    liste_data = request.body.split("&")
    for i in liste_data:
        response_data[i.split("=")[0]] = urllib.unquote_plus(i.split("=")[1])

    return response_data


def flag_report(receiver, message):
    url = "https://app.rapidpro.io/api/v2/broadcasts.json"
    data = {"urns": ["tel:" + receiver], "text": message}
    sending = requests.post(
        url,
        headers={
            "Content-type": "application/json",
            "Authorization": "Token %s" % settings.TOKEN,
        },
        data=json.dumps(data),
    )
    return sending.content


def email_report_flagged(receiver, message):
    try:
        email = EmailMessage("Report innacurate", message, to=[receiver])
        email.send()
    except Exception:
        raise Exception
    else:
        return "Sent"


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
