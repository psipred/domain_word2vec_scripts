from itertools import takewhile


def return_gap_name(start, stop):
    if (stop-start)+1 <= 100:
        return("G100")
    if (stop-start)+1 <= 200:
        return("G200")
    if (stop-start)+1 <= 300:
        return("G300")
    if (stop-start)+1 <= 400:
        return("G400")
    return("G500")


def handle_cache(data):
    splits = []
    for line in data:
        splits.append(line.split(","))

    sorted_data = sorted(splits, key=lambda x: x[6])
    protein_length = int(sorted_data[0][8])
    protein_name = sorted_data[0][0]
    # STRINGS: Domain names: PFXXXX,
    #          Gaps; G100 G200 G300 G400 G500
    #          Disorder gaps; DG100 DG200 DG300 DG400 DG500
    #          Low Complexity Gaps: LG100  LG200 LG300 LG400 LG500
    #          CoileCoil Gaps:  CG100  CG200 CG300 CG400 CG500

    # loop over the PF domains and construct a list of gaps and PFam domains
    previous_start = 0
    domain_size = len(list(takewhile(lambda x: x[5].startswith("PF"), sorted_data)))
    domains_and_gaps = []
    for idx, domain in enumerate(takewhile(lambda x: x[5].startswith("PF"), sorted_data)):
        if int(domain[6]) > previous_start+1:
            if ((int(domain[6])-1) - (previous_start+1)) > 20:
                gap_id = return_gap_name(previous_start+1, int(domain[6])-1)
                domains_and_gaps.append([gap_id, domain[0], previous_start+1, int(domain[6])-1])
            domains_and_gaps.append([domain[5], domain[0], domain[6], domain[7]])
        else:
            domains_and_gaps.append([domain[5], domain[0], domain[6], domain[7]])
        if idx+1 == domain_size:
            if int(domain[7]) < protein_length:
                if (protein_length - int(domain[7])) > 20:
                    gap_id = return_gap_name(int(domain[7]), protein_length)
                    domains_and_gaps.append([gap_id, domain[0], int(domain[7]), protein_length])
        previous_start = int(domain[7])

    #print(domains_and_gaps)
    for idx, region in enumerate(domains_and_gaps):
        if not region[0].startswith("PF"):
            for domain in sorted_data:
                if not domain[5].startswith("PF"):
                    if int(domain[6]) in range(int(region[2]), int(region[3])):
                        #print(domain)
                        if "G" in domains_and_gaps[idx][0][0]:
                            if domain[5].startswith("mobidb-lite"):
                                domains_and_gaps[idx][0] = "D"+domains_and_gaps[idx][0]
                            elif domain[5].startswith("Low"):
                                domains_and_gaps[idx][0] = "L"+domains_and_gaps[idx][0]
                            elif domain[5].startswith("Coiled"):
                                domains_and_gaps[idx][0] = "C"+domains_and_gaps[idx][0]

                        #rewrite first char in gap
    # now loop over the over regions and reannotated the gaps strings
    #print(domains_and_gaps)
    if len(domains_and_gaps) == 0:
        return
    output = domains_and_gaps[0][1]+": "
    for region in domains_and_gaps:
        output += region[0]+" "
    output = output.rstrip()
    print(output)

previous_uniprot = "XXX"
line_cache = []
with open("/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/"
          "final_domains_E.dat") as pfam:
#          "test.dat") as pfam:
    first_line = pfam.readline()
    first_line = first_line.rstrip()
    entries = first_line.split(",")
    line_cache.append(first_line)
    previous_uniprot = entries[0]

    for line in pfam:
        line = line.rstrip()
        entries = line.split(",")
        if entries[0] not in previous_uniprot:
            handle_cache(line_cache)
            line_cache = []
            line_cache.append(line)
            previous_uniprot = entries[0]
        else:
            line_cache.append(line)

handle_cache(line_cache)
