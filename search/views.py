from django.shortcuts import render
from django.http import JsonResponse
import os
import json
from freezer.settings import BASE_DIR

import datetime
import csv

master_file = "search/master_data.csv"

def home(request):
    return render(request, "home.html")

def search_code(code):
    file_path = os.path.join(BASE_DIR, 'search/master_data.csv')
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


# Create your views here.
def search_view(request):
    if request.POST:
        code_post = request.POST['cooler_no']
        data = search_code(code_post)
        if data is not None:
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


def cooler_verification(request, time_jump, center):
    # ***
    time_jump = time_jump
    center = center
    # ***
    date_jump = datetime.datetime.today() - datetime.timedelta(weeks=time_jump)
    row_list = []
    file_path = os.path.join(BASE_DIR, 'search/master_data.csv')
    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # date
                last_scanned = row['LAST SCANNED']
                scan_date = last_scanned
                distribution_center = row['OCCD TRADING NAME']

                if center != distribution_center:
                    continue

                last_scanned = datetime.datetime.strptime(last_scanned, '%Y-%m-%d')

                if last_scanned < date_jump and row['Lat'] != "#N/A" and row['Long'] != "#N/A":
                    geometry = {
                        "latitude": row['Lat'],
                        "longitude": row['Long'],
                        "rad": row['RAD NAME'],
                        "asm": row['ASM NAME'],
                        "last_scanned": scan_date,
                        "outlet_number": row['OUTLET NO'],
                        "outlet_name": row['CURRENT OUTLET NAME'],
                        "mobile_number": row['CURRENT MOBILE\TEL NO'],
                        "outlet_location": row['CURRENT LOCATION']
                    }
                    row_list.append(geometry)
                else:
                    # target ahead of date
                    pass
            except:
                pass

    data = json.dumps(row_list)
    context = {
        "row_list": data
    }

    return render(request, "cooler_verification.html", context)


def cooler_verification_blank(request):
    
    return render(request, "cooler_verification.html")
