#
import sys
import string
import json

"""
Clean up original json file to get rid of unicode chars.

Usage: python clean  inputJson  outputJson
"""

def process():
    fp = open(sys.argv[1],'r')
    jsonObj = json.load(fp)
    outFp = open(sys.argv[2],'w')
    json.dump(jsonObj, outFp, ensure_ascii=True, indent=2, \
				separators=(',',': '), sort_keys=True)

if __name__ == '__main__':
    process()
