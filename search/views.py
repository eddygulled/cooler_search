from django.shortcuts import render
from django.http import JsonResponse
import os, json
from freezer.settings import BASE_DIR

import csv

def search_code(code):
    file_path = os.path.join(BASE_DIR, 'search/master_data_11_10_2022.csv')
    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row['COOLER TAG'] == str(code) or row['OUTLET TAG'] == str(code):
                    return row
            except:
                pass
        
    return None

def record_data(request, tag, long, lat):
    file_path = os.path.join(BASE_DIR, 'search/geocoordinates.csv')
    data = [tag, long, lat]
    file = open(file_path, 'a')
    writer = csv.writer(file)
    writer.writerow(data)
    return JsonResponse({'status': 200})

# Create your views here.
def search_view(request):
    if request.POST:
        code_post = request.POST['cooler_no']
        data = search_code(code_post)
        if   data is not None:
            context = {
                'loaded': True,
                'map': False,
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
                'route_name': data['ROUTE NAME'],
                'current_location': data['CURRENT LOCATION'],
                'fi_system_status': data['FI System status']
            }
            return render(request, "index.html", context)
        else:
            print("not found")
            return render(request, "index.html", {'msg': 'nothing Found'}) 

    return render(request, "index.html")