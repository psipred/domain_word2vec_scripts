
mf_flag = False
with open('/scratch1/NOT_BACKED_UP/dbuchan/GO/gene_ontology.obo') as obo:
    for line in obo:
        line = line.rstrip()
        if line.startswith('namespace: molecular_function'):
            mf_flag = True
        if line.startswith('namespace: biological_process'):
            mf_flag = False
        if line.startswith('namespace: cellular_component'):
            mf_flag = False
        if line.startswith('relationship: part_of'):
            if not mf_flag:
                print(line)
        else:
            print(line)
