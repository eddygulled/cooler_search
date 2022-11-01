from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

import os
import json
from freezer.settings import BASE_DIR, MEDIA_ROOT
from .forms import MasterDataFileForm
from .models import MasterDataFile


import datetime
import csv

def get_recent_uploaded():
    uploads = MasterDataFile.objects.filter(active = True).order_by('-id')
    if uploads:
        return uploads[0]
    else:
        return None


def home(request):
    return render(request, "home.html")

def search_code(code):
    target_file = get_recent_uploaded()
    if target_file is None:
        return False
    file_path = os.path.join(BASE_DIR, "media/"+target_file.filename())

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
        if data is False:
            return redirect("/error")

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

    target_file = get_recent_uploaded()
    if target_file is None:
        return redirect("/error")

    file_path = os.path.join(BASE_DIR, "media/"+target_file.filename())

    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # date
                last_scanned = row['LAST SCANNED']
                scan_date = last_scanned
                distribution_center = row['OCCD TRADING NAME']
                rad_name = row['RAD NAME']

                if center != distribution_center:
                    continue

                last_scanned = datetime.datetime.strptime(last_scanned, '%Y-%m-%d')

                if last_scanned < date_jump:
                    
                    lat = row['Lat']
                    longs = row['Long']

                    geometry = {
                        "latitude": lat,
                        "longitude": longs,
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

def rad_cooler_verification(request, time_jump, center):
    # ***
    time_jump = time_jump
    center = center
    # ***
    date_jump = datetime.datetime.today() - datetime.timedelta(weeks=time_jump)
    row_list = []

    target_file = get_recent_uploaded()
    if target_file is None:
        return redirect("/error")

    file_path = os.path.join(BASE_DIR, "media/"+target_file.filename())

    file = open(file_path, 'r', encoding='utf-8', errors='ignore')
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # date
                last_scanned = row['LAST SCANNED']
                scan_date = last_scanned
                distribution_center = row['OCCD TRADING NAME']
                rad_name = row['RAD NAME']

                if center != rad_name:
                    continue

                last_scanned = datetime.datetime.strptime(last_scanned, '%Y-%m-%d')

                if last_scanned < date_jump:
                    
                    lat = row['Lat']
                    longs = row['Long']

                    geometry = {
                        "latitude": lat,
                        "longitude": longs,
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

def error(request):
    
    return render(request, "error.html")


def upload_file(request):
    if request.user.is_authenticated is not True:
        return redirect("/login")

    if request.method == 'POST':
        form = MasterDataFileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/upload")
    else:
        uploads = MasterDataFile.objects.all().order_by('-id')
        form = MasterDataFileForm()
    return render(request, "upload.html", {'form': form, 'uploads': uploads})


def login_view(request):
    if request.POST:
        _user_name = request.POST['username']
        _password = request.POST['password']

        user = authenticate(username=_user_name, password=_password)

        if user is not None:
            login(request, user)
            return redirect("/upload")
        else:
            return redirect("/login")
    else:
        return render(request, "login.html")


def activate_file_view(request, file_id):
    if request.user.is_authenticated is not True:
        return redirect("/login")
    # deactivate other files
    MasterDataFile.objects.all().update(active=False)
    # activate file
    file = MasterDataFile.objects.get(id=file_id)
    file.active = True
    file.save()
    return redirect("/upload")