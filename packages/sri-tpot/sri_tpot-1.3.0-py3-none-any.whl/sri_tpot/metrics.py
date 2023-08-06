# -*- coding: utf-8 -*-

"""This file is part of the TPOT library.

TPOT was primarily developed at the University of Pennsylvania by:
    - Randal S. Olson (rso@randalolson.com)
    - Weixuan Fu (weixuanf@upenn.edu)
    - Daniel Angell (dpa34@drexel.edu)
    - and many more generous open source contributors

TPOT is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

TPOT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with TPOT. If not, see <http://www.gnu.org/licenses/>.

"""

import numpy as np
from sklearn.metrics import make_scorer, SCORERS
from sklearn.metrics import jaccard_similarity_score, f1_score, mean_squared_error
from math import sqrt

def balanced_accuracy(y_true, y_pred):
    """Default scoring function: balanced accuracy.

    Balanced accuracy computes each class' accuracy on a per-class basis using a
    one-vs-rest encoding, then computes an unweighted average of the class accuracies.

    Parameters
    ----------
    y_true: numpy.ndarray {n_samples}
        True class labels
    y_pred: numpy.ndarray {n_samples}
        Predicted class labels by the estimator

    Returns
    -------
    fitness: float
        Returns a float value indicating the individual's balanced accuracy
        0.5 is as good as chance, and 1.0 is perfect predictive accuracy
    """
    all_classes = list(set(np.append(y_true, y_pred)))
    all_class_accuracies = []
    for this_class in all_classes:
        this_class_sensitivity = 0.
        this_class_specificity = 0.
        if sum(y_true == this_class) != 0:
            this_class_sensitivity = \
                float(sum((y_pred == this_class) & (y_true == this_class))) /\
                float(sum((y_true == this_class)))

            this_class_specificity = \
                float(sum((y_pred != this_class) & (y_true != this_class))) /\
                float(sum((y_true != this_class)))

        this_class_accuracy = (this_class_sensitivity + this_class_specificity) / 2.
        all_class_accuracies.append(this_class_accuracy)

    return np.mean(all_class_accuracies)

def f1_true(y_true, y_pred):
    if hasattr(y_true, 'iloc'):
        y_true = y_true.iloc[:, 0].tolist()
    y_true = [ int(x) for x in y_true ]
    y_pred = [ int(x) for x in y_pred ]
    return f1_score(y_true, y_pred)

def root_mean_squared_error(y_true, y_pred):
    return sqrt(mean_squared_error(y_true, y_pred))

def root_mean_squared_error_average(y_true, y_pred):
    #TODO: How do we average these values, dont we need them all to do this?
    return sqrt(mean_squared_error(y_true, y_pred))


SCORERS['balanced_accuracy'] = make_scorer(balanced_accuracy, greater_is_better=True)
SCORERS['jaccard_similarity_score'] = make_scorer(jaccard_similarity_score, greater_is_better=True)
SCORERS['f1_true'] = make_scorer(f1_true, greater_is_better=True)
SCORERS['mean_squared_error'] = make_scorer(mean_squared_error, greater_is_better=False)
SCORERS['root_mean_squared_error'] = make_scorer(root_mean_squared_error, greater_is_better=False)
SCORERS['root_mean_squared_error_average'] = make_scorer(root_mean_squared_error_average, greater_is_better=False)
