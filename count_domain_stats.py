import csv

domains = set()
proteins = set()

with open("final_domains_E.dat", "r") as domainfh:
    domainreader = csv.reader(domainfh, delimiter=',')
    for entries in domainreader:
        try:
            domains.add(entries[5])
            proteins.add(entries[0])
        except:
            print(entries)

print("No of Proteins:", len(proteins))
print("No of Domains:", len(domains))


# combined_domains_E.dat
# No of Proteins: 11182544
# No of Domains: 11411

# final_domains_E.dat
# No of Proteins: 11182544
# No of Domains: 11355

