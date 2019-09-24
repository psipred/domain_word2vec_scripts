import csv

duf_file = "duf_annotations.csv"

with open(duf_file) as duf_data:
    duf_reader = csv.reader(duf_data, delimiter=',')
    for row in duf_reader:
        print(row[0], len(row)-1, sep=",")
