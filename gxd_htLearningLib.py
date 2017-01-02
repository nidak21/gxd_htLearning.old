'''
Common stuff for applying sklearn to gxd High Throughput experiment indexing
'''
import sys

from sklearn.datasets import load_files
from sklearn import metrics

from sklearnHelperLib import orderTargets


def getTrainingSet():
    
    # sklearn training set folder structure for now
    # The training data folder must be passed as first argument
    dataset = load_files(sys.argv[1])
    orderTargets(dataset, ['yes', 'no'])

    return dataset
# end getTrainingSet() ---------------------------

def getFormatedMetrics( y_test,	# true category assignments for test set
		y_predicted,	# predicted assignments
		target_names	# the names of the categories
		):
    '''
    Return formated metrics report
    y_test and y_predicted are lists of integer category indexes.
    target_names[i] is the name (string) of the i'th category.
    '''
    output = "%s\n\n" % metrics.classification_report(y_test, y_predicted,
					    target_names = target_names)

    output += "%s\n" % getFormatedCM(y_test, y_predicted, target_names)

    return output
# end getFormatedMetrics() ---------------------------

def getFormatedCM( y_test,	# true category assignments for test set
		y_predicted,	# predicted assignments
		target_names	# the names of the categories
		):
    '''
    Return formated confusion matrix
    '''
    output = "%s\n%s\n" % ( str(target_names),
			str(metrics.confusion_matrix(y_test, y_predicted)) )
    return output
# end getFormatedMetrics() ---------------------------
