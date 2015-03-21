import datetime
from django.db.models.query import QuerySet, ValuesQuerySet
from django.http import HttpResponse
import csv
from pytz import timezone
timezone('Africa/Bujumbura')

class ExcelResponse(HttpResponse):
    def __init__(self, data, output_name='Report_Muco', headers=None,
                 force_csv=False, encoding='utf8', font=''):
        valid_data = False
        if isinstance(data, ValuesQuerySet):
            data = list(data)
        elif isinstance(data, QuerySet):
            data = list(data.values())
        if hasattr(data, '__getitem__'):
            if isinstance(data[0], dict):
                if headers is None:
                    headers = data[0].keys()
                data = [[row[col] for col in headers] for row in data]
                data.insert(0, headers)
            if hasattr(data[0], '__getitem__'):
                valid_data = True
        assert valid_data is True, "ExcelResponse requires a sequence of sequences"

        import StringIO
        output = StringIO.StringIO()
        writer = csv.writer(output)
        writer.writerows(data)
        content_type = 'text/csv'
        file_ext = 'csv'
        output.seek(0)
        super(ExcelResponse, self).__init__(content=output.getvalue(),
                                            content_type=content_type)
        self['Content-Disposition'] = 'attachment;filename="%s.%s.%s"' % \
            (output_name.replace('"', '\"'), datetime.datetime.now().strftime("%d %b %Y  %p"), file_ext )
