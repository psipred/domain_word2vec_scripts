import csv

go_assigns = '/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/pfam_go_mapping.csv'

print("Counts")
with open(go_assigns, 'r') as go:
    goreader = csv.reader(go, delimiter=',', quotechar='|')
    for row in goreader:
        print(len(row)-1)
