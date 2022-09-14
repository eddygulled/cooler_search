import csv


file = open("test/user.csv")

mobile = "salum Rajabu"

with file as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['name'] == mobile:
            print(row)
