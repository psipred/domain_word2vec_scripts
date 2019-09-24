import csv
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# parse protein2ipr to output just the pfam domains
def output_domains(name, sorted_domains, previous_length, region_start):
    last_size = 0
    for domain in sorted_domains:
        gap_length = domain[0]-region_start
        if gap_length > 14 and gap_length < 5000:
            # pass
            print(name+","+str(gap_length))
        if gap_length > 20000:
            eprint("GAP LENGTH LARGE: 1")
            eprint(name+":"+str(gap_length))
        region_start = domain[1]
    gap_length = previous_length-region_start  # get the last segment
    if gap_length > 14 and gap_length < 5000:
        # pass
        print(name+","+str(gap_length))
    if gap_length > 20000:
        eprint("GAP LENGTH LARGE: 2")
        eprint(name+":"+str(gap_length))


my_coords = []
count = 0
region_start = 1
previous_protein = "XXXX"
previous_length = 0
with open('/scratch0/NOT_BACKED_UP/dbuchan/projects/interpro_word2vec/'
#          'test.csv') as pfam:
          'taxa_annotated_ipr_pfam_assignments.csv') as pfam:
    pfamreader = csv.reader(pfam, delimiter=',', quotechar='|')
    for row in pfamreader:
        if count == 0:
            previous_protein = row[0]
            previous_length = int(row[8])
            my_coords.append([int(row[6]), int(row[7])])
            count = 1
            # print(row)
            continue
        if row[0] != previous_protein:
            # do stuff
            sorted_domains = sorted(my_coords, key=lambda x: (x[0]))
            # print(sorted_domains)
            output_domains(previous_protein, sorted_domains, previous_length, region_start)

            region_start = 1
            my_coords = []
            previous_protein = row[0]
            previous_length = int(row[8])
        if len(row) != 9:
            eprint("ROW LENGTH ERROR")
            eprint(row)
            # exit()
        try:
            my_coords.append([int(row[6]), int(row[7])])
        except Exception as e:
            eprint("CAN'T CAST COORDS")
            eprint(row)
            # exit()
        # print(row)
    sorted_domains = sorted(my_coords, key=lambda x: (x[0]))
    output_domains(previous_protein, sorted_domains, previous_length, region_start)
