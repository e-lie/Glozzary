import csv

with open('Métonymies gouvernements.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
