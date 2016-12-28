"""
Play with classifying GXD high throughput experiment indexing using
scikit-learn.
Try several different learning algorithms and compare them.

Inputs are text files with Array Express experiment titles and descriptions.
Try to classify them as 'yes' or 'no' (relevant to GXD or not)
"""
# Author: Jim Kadin

import sys

from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import metrics

from sklearnHelperLib import orderTargets

# The training data folder must be passed as first argument
data_folder = sys.argv[1]
dataset = load_files(data_folder)
orderTargets(dataset, ['yes', 'no'])

# Split the dataset in training and test set:
docs_train, docs_test, y_train, y_test = train_test_split(
				dataset.data, dataset.target, test_size=0.5)


# define vectorizer and set of params to optimize over
# characters instead of word tokens. 1, 2, and 3 word ngrams.
cv = TfidfVectorizer(analyzer='word',ngram_range=(1,3), stop_words='english' )
			# option: strip_accents='ascii' or 'unicode' or 'None'j
vectorizerParams = {'vect__ngram_range': [ (1,1), (1,2), (1,3), (1,4) ],
	            'vect__stop_words':  [ 'english', None ],
	      }
# define classifiers and their params to optimize over
classifiers = [ 
		('Perceptron'    , Perceptron(),    {} ),
		('MultinomialNB' , MultinomialNB(), {}),
		('SGDClassifier' , SGDClassifier(loss='hinge', penalty='l2',
					alpha=1e-3, n_iter=5, random_state=42),
					{'clf__n_iter': [5,7,10]} ),
	      ]

for classifierName, clf, params in classifiers:
    print
    print classifierName
    params.update(vectorizerParams )
    
    gs = GridSearchCV( Pipeline( [('vect', cv), ('clf', clf)] ), params )

    gsout = gs.fit(docs_train, y_train)
    print gsout.best_score_
    print gsout.best_params_

    trainedClf = gs.best_estimator_

    # TASK: Predict the outcome on the testing set
    y_predicted = trainedClf.predict( docs_test )

    # Print the classification report
    print(metrics.classification_report(y_test, y_predicted,
					target_names=dataset.target_names))
    # Plot the confusion matrix
    print dataset.target_names
    cm = metrics.confusion_matrix(y_test, y_predicted)
    print(cm)
