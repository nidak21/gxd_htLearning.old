'''
Common stuff for applying sklearn to gxd High Throughput experiment indexing

Primarily the functions in here know about the labels ('yes' and 'no') for
evaluating HT experiment indexing, including the order of these labels in
the dataset labels.

This should become a class.
'''
import sys

from sklearn.datasets import load_files
from sklearn import metrics

from sklearnHelperLib import orderTargets

# in the list of labels for evaluating text data for inclusing into GXD...
INDEX_OF_YES = 1
INDEX_OF_NO = 0

def getTrainingSet():

    # sklearn training set folder structure for now
    # The training data folder must be passed as first argument
    dataset = load_files(sys.argv[1])
    #orderTargets(dataset, ['yes', 'no'])	# to reorder these, skip it

    return dataset
# end getTrainingSet() ---------------------------

def getFormatedMetrics( \
	y_true,		# true category assignments for test set
	y_predicted,	# predicted assignments
        scorer_name,    # what to call the scorer function
        score_value     # score value to report
                        # NOTE would prefer to pass scorer function itself,
                        #    but could not get it to work,
                        #    tried metrics.make_scorer() various ways, but nogo
		):
    '''
    Return formated metrics report
    y_true and y_predicted are lists of integer category indexes.
    target_names[i] is the name (string) of the i'th category.
    '''
    #output = "%s: %5,3d\n%s\n" % (scorer_name, score_value,
    output = "%s\n" % ( \
                    metrics.classification_report(y_true, y_predicted,
				labels=[INDEX_OF_YES],target_names=["yes"]) )

    output += "%s\n" % getFormatedCM(y_true, y_predicted)

    return output
# end getFormatedMetrics() ---------------------------

def getFormatedCM( y_true,	# true category assignments for test set
		y_predicted	# predicted assignments
		):
    '''
    Return formated confusion matrix
    '''
    output = "%s\n%s\n" % ( \
		str( ['yes', 'no']),
		str( metrics.confusion_matrix(y_true, y_predicted,
			labels=[INDEX_OF_YES,INDEX_OF_NO])
		) )
    return output
# end getFormatedMetrics() ---------------------------
