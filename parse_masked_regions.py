from Bio import SeqIO
import re

re_string = "\|(.+)\|"

def parse_file(path, dom_type):
    for record in SeqIO.parse(path, "fasta"):
        if "..." in record.seq:
            raw_desc = record.description.replace(record.name+" ", "")
            raw_desc = raw_desc.replace(",", "")
            result = re.search(re_string, record.name)
            uniprot_id = result.group(1)
            for m in re.finditer(r'\.{3,}', str(record.seq)):
                print(uniprot_id+"\tIPRXXXXXX\t"+raw_desc+"\t"+dom_type+"\t" +
                      str(m.start()+1)+"\t"+str(m.end()+1))
            # return()


parse_file("/scratch1/NOT_BACKED_UP/dbuchan/interpro/"
           "uniprot_trembl_lc_masked.fasta", "LowComplexity")
parse_file("/scratch1/NOT_BACKED_UP/dbuchan/interpro/"
           "uniprot_trembl_cc_masked.fasta", "CoiledCoil")
