
def return_dom_type(dom_name):
    if dom_name.startswith("PF"):
        return("pfam")
    if dom_name.startswith("Coiled"):
        return("cc")
    if dom_name.startswith("Low"):
        return("lc")
    if dom_name.startswith("mobidb"):
        return("disorder")


def handle_cache(data):
    prot_length = 0

    accepted_lines = []
    for idx, line in enumerate(data):
        line = line.rstrip()
        accepted = True
        entries = line.split(",")
        if len(entries) < 8:
            continue
        len1 = int(entries[7])-int(entries[6])
        dom_type = return_dom_type(entries[5])
        if len(entries) == 9:
            prot_length = entries[8]
        for idx2, line2 in enumerate(data):
            if idx == idx2:
                continue  # don't compare like to like
            entries2 = line2.split(",")
            if len(entries2) < 8:
                continue
            len2 = int(entries2[7])-int(entries2[6])
            dom_type2 = return_dom_type(entries2[5])

            if int(entries[6]) in range(int(entries2[6]), int(entries2[7])+1) \
               or int(entries[7]) in \
               range(int(entries2[6]), int(entries2[7])+1):
                # in here we know 1st domain overlaps with this next one
                if "pfam" in dom_type:
                    if "pfam" in dom_type2:
                        if len1 < len2:
                            accepted = False
                if "disorder" in dom_type:
                    if "pfam" in dom_type2:
                        accepted = False
                    if "disorder" in dom_type2:
                        if len1 < len2:
                            accepted = False
                if dom_type == "cc":
                    if "pfam" in dom_type2 or "disorder" in dom_type2:
                        accepted = False
                    if "cc" in dom_type2:
                        if len1 < len2:
                            accepted = False
                if dom_type == "lc":
                    if "pfam" in dom_type2 or "disorder" in dom_type2 or \
                      "cc" in dom_type2:
                        accepted = False
                    if "lc" in dom_type2:
                        if len1 < len2:
                            accepted = False
        if accepted:
            accepted_lines.append(line)

    for line in accepted_lines:
        line = line.rstrip()
        entries = line.split(",")
        if len(entries) == 9:
            print(line)
        else:
            print(line+","+str(prot_length))


previous_uniprot = "XXX"
line_cache = []
# with open("/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/"
#          "combined_domains_E.dat") as pfam:
with open("combined_domains_E.dat") as pfam:
    first_line = pfam.readline()
    entries = first_line.split(",")
    line_cache.append(first_line)
    previous_uniprot = entries[0]

    for line in pfam:
        entries = line.split(",")
        if entries[0] not in previous_uniprot:
            handle_cache(line_cache)
            line_cache = []
            line_cache.append(line)
            previous_uniprot = entries[0]
        else:
            line_cache.append(line)

handle_cache(line_cache)
