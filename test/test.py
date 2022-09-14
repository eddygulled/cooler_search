import csv

def search_code(code):
    file = open("coolerdata.csv")
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['OUTLET NO'] == str(code):
                return row
        
    return None

data = search_code(5047333)
print(data)
