import numpy as np
from numpy.random import choice
from sklearn.utils.validation import indexable, _num_samples
from itertools import combinations

class LeavePairOut:
    '''
    Splits the data into train-test by leaving 2 samples out in each CV-fold with an option of
    returning only those test pairs with matching group labels
    '''
    def split(self, X, y, erry=None, groups=None, match_groups=False, 
             match_window=None, orderN=False, random_state=None):
        '''
        Parameters:
        -----------
        X: array-like, shape=(n_samples, n_features)
            data matrix
        y: array-like, shape=(n_samples)
            class labels
        erry: float or array-like
            error in y for regression problems, must be non-negative real number(s)
            will return test pairs for which 
                abs(y[i]-y[j]) >= erry, if erry is scalar) 
                abs(y[i]-y[j]) >= max(erry[i], erry[j]), if  erry is array-like
        groups: array-like, shape=(n_samples)
            group labels
        match_groups: bool, default=False
            if True then returns train test split such that test pairs have the same 
            group labels
        match_window: float, default=None
            the allowed window for matching the groups when the groups are 
            float values
            if match_groups is True and match_window is specified, it will return 
            entries for which  abs(groups[i]-groups[j]) < match_window)
        orderN: bool, default=False
            if True then randomly pick O(N) test pairs, if match_groups is True then 
            the random pairs have the same group labels
        random_state: float, default=None
            if specified the function returns the same randomly picked O(N) test
            pairs, redundant when orderN=False.
        Returns:
        --------
        train and test indices
        '''
        X, y, groups = indexable(X, y, groups)
        num_samples = _num_samples(X)
        if num_samples<2: 
            raise ValueError ('Number of samples must be greater than or equal to 2.') 
        if groups is None and match_groups is True:
            raise ValueError ('Argument "groups" should be specified if "match_groups" is True.')
        if erry is None:
            erry = np.zeros(num_samples, dtype=float)
        if type(erry) is float or type(erry) is int:
            erry = np.full_like(np.arange(num_samples, dtype=float), erry)
        if type(match_window) is int or type(match_window) is float:
            match_window = np.full_like(np.arange(num_samples, dtype=float), 
                                        match_window)
        return self.train_test_indices(X, y, erry, groups, match_groups, 
                                       match_window, orderN, random_state)


    def train_test_indices(self, X, y, erry, groups, match_groups, 
                            match_window, orderN, random_state):
        num_samples = _num_samples(X)
        indices = np.arange(num_samples)
        if orderN is False:
            for i, j in combinations(range(num_samples), 2):
                if match_groups is True:
                    if (match_window is None and groups[i] != groups[j]):
                        continue
                    elif (match_window.any() is not None and \
                    (abs(groups[i]-groups[j]) > min(match_window[i], match_window[j]))):
                        continue
                if abs(y[i] - y[j]) < max(erry[i], erry[j]):
                    continue
                test_index = np.array([i, j])
                test_mask = np.zeros(num_samples, dtype=bool)
                test_mask[test_index] = True
                train_index = indices[np.logical_not(test_mask)]
                yield  train_index, test_index
        else:
            for i in indices:
                if match_groups is False:
                    try:
                        if random_state is not None:
                            r = np.random.RandomState(random_state+i)
                            j = r.choice([k for k in indices if i!=k and \
                                        abs(y[i]-y[k]) >= max(erry[i], erry[k])])
                        else:
                            j = choice([k for k in indices if i!=k and \
                                abs(y[i]-y[k]) >= max(erry[i], erry[k])])
                    except ValueError:
                        continue
                else:
                    if match_window is None:
                        try:
                            if random_state is not None:
                                r = np.random.RandomState(random_state+i)
                                j = r.choice([k for k in indices if i!=k and \
                                      groups[i] == groups[k] and \
                                      abs(y[i]-y[k]) >= max(erry[i], erry[k])])
                            else:
                                j = choice([k for k in indices if i!=k and \
                                    groups[i] == groups[k] and \
                                    abs(y[i]-y[k]) >= max(erry[i], erry[k])])
                        except ValueError:
                            continue
                    else:
                        try:
                            j = choice([k for k in indices if i!=k and \
                            abs(groups[i]-groups[k]) <= min(match_window[i], 
                            match_window[k]) and \
                            abs(y[i]-y[k]) >= max(erry[i], erry[k])])
                        except ValueError:
                            continue
                
                test_index = np.array([i,j])
                test_mask = np.zeros(num_samples, dtype=bool)
                test_mask[test_index] = True
                train_index = indices[np.logical_not(test_mask)]
                yield  train_index, test_index

