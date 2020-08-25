"""
This script is to parse a fixed width file using Python For LFS test
Command run: 
python Parse_Lfs.py -i IpFile.txt -o OpFile_Name.csv -c Spec.txt -d ,
Inputs are as follows
1. Input FIle - Mandatory(Argument -i - File which has column names and fixed Width data in it)
2. Output File - Optional (Argument -o, if not provided output filename will be used as InputFIleName.Delimited.csv)
3. Spec File - Optional (Argument -c, config file, if not provided will look for Spec.txt file on same path, if not present script will not run)
    Config Format as :
    FieldName,fieldLength
    eg:
    f1,5
    f2,12
    etc:
4. Delimiter - Optional (Argument -d, if not provided default value is "," (comma))
"""
from collections import OrderedDict
import argparse
from argparse import ArgumentParser
import os.path
import sys


def slices(s, args):
    position = 0
    for length in args:
        length = int(length)
        yield s[position:position + length]
        position += length

def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x

parser = ArgumentParser(description="Please provide your Inputs as -i InputFile -o OutPutFile -c ConfigFile")
parser.add_argument("-i", dest="InputFile", required=True,    help="Provide your Input file name here, if file is on different path than where this script resides then provide full path of the file", metavar="FILE", type=extant_file)
parser.add_argument("-o", dest="OutputFile", required=False,    help="Provide your Output file name here, if file is on different path than where this script resides then provide full path of the file", metavar="FILE")
parser.add_argument("-c", dest="ConfigFile", required=False,   help="Provide your Config file name here,File should have value as fieldName,fieldLength. if file is on different path than where this script resides then provide full path of the file", metavar="FILE",type=extant_file)
parser.add_argument("-d", dest="Delimiter", required=False,   help="Provide the delimiter string you want",metavar="STRING", default=",")

args = parser.parse_args()

#Input file madatory
InputFile = args.InputFile
#Delimiter by default "|"
DELIMITER = args.Delimiter

#Output file checks
if args.OutputFile is None:
    OutputFile = str(InputFile) + "Delimited.csv"
    print ("Setting Ouput file as "+ OutputFile)
else:
    OutputFile = args.OutputFile

#Config file check
if args.ConfigFile is None:
    if not os.path.exists("Spec.txt"):
        print ("There is no Config File provided exiting the script")
        sys.exit()
    else:
        ConfigFile = "Spec.txt"
        print ("Taking Spec.txt file on this path as Default Config File")
else:
    ConfigFile = args.ConfigFile

fieldNames = []
fieldLength = []
myvars = OrderedDict()


with open(ConfigFile) as myfile:
    for line in myfile:
        name, var = line.partition(",")[::2]
        myvars[name.strip()] = int(var)
for key,value in myvars.items():
    fieldNames.append(key)
    fieldLength.append(value)

with open(OutputFile, 'w') as f1:
    fieldNames = DELIMITER.join(map(str, fieldNames))
    f1.write(fieldNames + "\n")
    with open(InputFile, 'r') as f:
        for line in f:
            rec = (list(slices(line, fieldLength)))
            myLine = DELIMITER.join(map(str, rec))
            f1.write(myLine + "\n")

