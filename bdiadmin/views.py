from jsonview.decorators import json_view
from bdiadmin.models import *
from django.http import JsonResponse
import json


@json_view
def get_commune(request, pk):

    communes = []
    for i in Commune.objects.filter(province=pk).values('id', 'name'):
        communes.append({i['id']: i['name']})
    return JsonResponse(json.dumps(communes), safe=False)


@json_view
def get_colline(request, pk):
    collines = []
    for i in Colline.objects.filter(commune=pk).values('id', 'name'):
        collines.append({i['id']: i['name']})
    return JsonResponse(json.dumps(collines), safe=False)