from collections import defaultdict
accessions = []
valid_codes = ['EXP', 'IBA', 'IDA', 'IEP', 'IGC', 'IGI', 'IMP', 'IPI']
results = defaultdict(list)

with open('/scratch1/NOT_BACKED_UP/dbuchan/uniprot/'
          'uniprot_trembl.dat') as uniprot:
#          'test.dat') as uniprot:
    for line in uniprot:
        line = line.rstrip()
        if line.startswith("AC"):
            accessions = line[5:].split("; ")
            accessions = [s.strip(";") for s in accessions]
        if line.startswith("DR   GO;"):
            entries = line[9:].split("; ")
            code = entries[2].split(":")
            # print(accessions)
            # print(line)
            if code[0] in valid_codes:
                for accession in accessions:
                    results[accession].append(",".join([accession, entries[0], code[0]]))

for accession in results:
    for line in results[accession]:
        print(line)
