from django.shortcuts import render
import os, json
from freezer.settings import BASE_DIR

import csv

def search_code(code):
    file_path = os.path.join(BASE_DIR, 'search/coolerdata.csv')
    file = open(file_path)
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['OUTLET NO'] == str(code):
                    return row
            except:
                pass
        
    return None

# Create your views here.
def search_view(request):
    if request.POST:
        code_post = request.POST['cooler_no']
        data = search_code(code_post)
        context = {
            'loaded': True,
            'outlet_no': data['OUTLET NO'],
            'outlet_name': data['CURRENT OUTLET NAME'],
            'outlet_location': data['CURRENT LOCATION'],
            'mobile_number': data['CURRENT MOBILE\TEL NO'],
            'description_model': data['Description MODEL ID'],
            'cooler_tag': data['COOLER TAG'],
            'region': data['REGION'],
            'rad_name': data['RAD NAME'],
            'asm_name': data['ASM NAME'],
            'occd_training_name': data['OCCD TRADING NAME'],
            'last_scanned': data['LAST SCANNED'],
            'route_name': data['ROUTE NAME']
        }
        return render(request, "index.html", context)

    return render(request, "index.html")