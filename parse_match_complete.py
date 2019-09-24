# import xml.etree.cElementTree
import xml.etree.ElementTree as ElementTree

# get an iterable
context = ElementTree.iterparse('/scratch1/NOT_BACKED_UP/dbuchan/interpro/'
                                'match_complete.xml', events=("start", "end"))

# turn it into an iterator
context = iter(context)

# get the root element
event, root = next(context)

for event, protein in context:
    if event == "end" and protein.tag == "protein":
        # print(elem.attrib['id'])
        for match in protein:
            if 'MOBIDBLT' in match.attrib['dbname']:
                for coords in match:
                    print(protein.attrib['id']+"\tIPRXXXXXX\t" +
                          match.attrib['name']+"\t"+match.attrib['id']+"\t" +
                          coords.attrib['start']+"\t"+coords.attrib['end'])
        # exit()
        root.clear()
