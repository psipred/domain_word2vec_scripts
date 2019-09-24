import csv
import re
# parse protein2ipr to output just the pfam domains

length_lookup = {}
featre = re.compile(r'<protein id="(.+)"\sname=".+"\slength="(.+)"\scrc64')
with open("/scratch1/NOT_BACKED_UP/dbuchan/interpro/match_complete.xml") as itrfile:
    for line in itrfile:
        feat_matches = featre.search(line)
        if feat_matches:
            length_lookup[feat_matches.group(1)] = feat_matches.group(2)

with open('/scratch1/NOT_BACKED_UP/dbuchan/interpro/protein2ipr.dat') as csvfile:
    iprreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in iprreader:
        if row[3].startswith("PF"):
            row[2] = row[2].replace(',', '')
            if row[0] in length_lookup:
                print(",".join(row)+","+length_lookup[row[0]])
