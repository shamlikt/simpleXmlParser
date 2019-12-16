'''This is simple script to convert/mask XML

requirements:
------------
xmltodict

Usange: python3 xmlParser.py --input sample.xml --output output.xml --mask
        python3 xmlParser.py --input sample.xml --output output.json --json
        python3 xmlParser.py --input sample.xml --output output.json --json --mask
'''


import os
import json
import hashlib 
import argparse
import xmltodict
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import tostring
from pprint import pformat

NAMESPACE = "{urn:hl7-org:v3}"
FAMILY_TAG = "family"
NAME_TAG = "given"


class XmlTaskException(Exception):
    '''Custom Error'''
    pass

def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', '--input', action="store", default="sample.xml", required=True,
                       help='''input file''')

    parse.add_argument('-o', '--output', action="store", default="output.xml",
                       help='''output file''')

    parse.add_argument('-j', '--json', action="store_true", default=False,
                       help='''output file''')

    parse.add_argument('-m', '--mask', action="store_true", default=False,
                       help='''maskwith RandomValue''')
    return parse.parse_args()

def parse_xml(filename):
    ''' Parse the xml and return the xmltree Obj
    '''
    if not os.path.exists(filename):
        raise XmlTaskException('"{}" not Found'.format(filename))
    return ET.parse(filename)

def change_text(xmltree, custom_addr):
    ''' Mask the value with md5 hash
    '''
    tags = xmltree.findall('.//{}{}'.format(NAMESPACE, custom_addr))
    for tag in tags:
        tag.text = get_hash(tag.text)
    return xmltree

def write_output(file_name, data):
    ''' Dump data to file
    '''
    with open(file_name, "w") as f:
        f.write(data)
    
def get_hash(value):
    b_value = value.encode('utf-8')
    return hashlib.md5(b_value).hexdigest()

def main():
    args = parse_args()
    input_file = args.input
    output_file = args.output
    is_json = args.json
    is_mask = args.mask

    xmlTree = parse_xml(input_file)
    if is_mask:
        xmlTree = change_text(xmlTree, FAMILY_TAG)
        xmlTree = change_text(xmlTree, NAME_TAG)

    s_xmlTree = tostring(xmlTree.getroot())
    if is_json:
        xmlJson = json.dumps(xmltodict.parse(s_xmlTree))
        write_output(output_file, xmlJson)
    else:
        write_output(output_file, s_xmlTree.decode('utf-8'))

if __name__ == "__main__":
    main()
