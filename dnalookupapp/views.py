from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dnalookupapp.models import Protein
import json

# Create your views here.
@csrf_exempt
def filter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        look_key = data['code']
        proteins = Protein.objects.all()

        results = []
        found = False
        for p in proteins:
            seq = p.seq
            i = seq.find(look_key)
            while i != -1:
                found = True
                result = {
                    "name": p.name,
                    "ref": p.ref,
                    "seq": p.seq,
                    "index": i,
                    "id": data['id']
                }
                results.append(result)

                break
                i = seq.find(look_key, i + 1)
            if found:
                break
        response = {
            "data": results,
            "found": found
        }

        return JsonResponse(response)

@csrf_exempt
def sequence(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        data["seq"] = data["seq"].replace('\n', '')
        data["seq"] = data["seq"].replace('\r', '')
        protein = Protein(name=data["name"], ref = data["ref"], seq = data["seq"] )
        protein.save()
    return HttpResponse("request")