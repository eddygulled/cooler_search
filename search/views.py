from django.shortcuts import render
import os
from freezer.settings import BASE_DIR

import csv

def search_code(code):
    file_path = os.path.join(BASE_DIR, 'search/coolerdata.csv')
    file = open(file_path)
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['OUTLET NO'] == str(code):
                return row
        
    return None

# Create your views here.
def search_view(request):
    data = search_code(5037630)
    return render(request, "index.html", {'data': data})