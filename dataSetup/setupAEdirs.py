#!venv/bin/python
import sys
import string
import json

#DATAPATH="data"
DATAPATH="."
YESPATH = DATAPATH + '/yes'
NOPATH  = DATAPATH + '/no'

usageText = \
"""
Put Array Express GXT HT "yes/no" evaluation data into scikit text
directory/file structure for machine learning.
For each learning category (yes/no in this case), want one folder holding
the text files of inputs in that category.

Usage: python %s experiment_json_file yesfile nofile
	yesfile - IDs of known 'yes' experiments
	nofile  - IDs of known 'no' experiments
	Writes 'yes' experiments to %s
	Writes 'no'  experiments to %s
""" % (sys.argv[0],YESPATH, NOPATH)

def usage():
    sys.stderr.write(usageText)
    exit(5)

# NOT USED HERE
def hasMouse( orgs	# [ org names, ...]
		):
    for org in orgs:
	if org.lower() == 'mus musculus': return True
    return True


def process():
    try:
	fp = open(sys.argv[1],'r')
	jsonObj = json.load(fp,'utf-8')
	yesFp = open(sys.argv[2],'r')
	noFp = open(sys.argv[3],'r')
    except:
	sys.stderr.write("\n")
	(excType, value, traceback) = sys.exc_info()
	sys.stderr.write("%s %s\n" % (excType, value))
	usage()

    # build dict from accession to title/description together
    acc2exp = {}
    for exp in jsonObj['experiments']['experiment']:

	acc = exp['accession'].strip()
	title = exp['name']
	if type(title) == type([]) or type(title) == type({}) or title==None:
	    sys.stderr.write("%s skipped because weird name json\n" % acc)
	    continue
	desc = exp['description']['text']
	if type(desc) == type([]) or type(desc) == type({}) or desc==None:
	    sys.stderr.write("%s skipped because weird desc json\n" % acc)
	    continue
	try:
	    acc2exp[acc] = title.encode('utf-8').strip() + "\n" \
				    + desc.encode('utf-8').strip() + "\n"
	except:
	    sys.stderr.write("\n")
	    sys.stderr.write("ID = %s\n" % acc)
	    #(excType, value, traceback) = sys.exc_info()
	    #sys.stderr.write("%s %s\n" % (excType, value))
	    #exit(5)
	    raise

    for id in yesFp:
	acc = id.strip()
	if acc2exp.has_key(acc):
	    filename = YESPATH + '/' + acc
	    fp = open(filename, 'w')
	    fp.write(acc2exp[acc])
	    fp.close()
	else:
	    print "ID for 'yes' experiment not found in json file: '%s'" % acc


    for id in noFp:
	acc = id.strip()
	if acc2exp.has_key(acc):
	    filename = NOPATH + '/' + acc
	    fp = open(filename, 'w')
	    fp.write(acc2exp[acc])
	    fp.close()
	else:
	    print "ID for 'no' experiment not found in json file: '%s'" % acc
if __name__ == '__main__':
    process()
