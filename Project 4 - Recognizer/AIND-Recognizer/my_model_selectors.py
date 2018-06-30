import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        best_model = None
        best_score = float('inf')
        logN = np.log(len(self.X))

        for number_of_states in range(self.min_n_components, self.max_n_components + 1):
            try:
                hmm_model = self.base_model(number_of_states)
                logL = hmm_model.score(self.X, self.lengths)

                p = (number_of_states * number_of_states) + (number_of_states * hmm_model.n_features * 2) - 1
                score = -2 * logL + p * logN
            except:
                continue
            
            if score < best_score:
                best_score = score
                best_model = hmm_model

        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores

        best_score = float('-inf')
        best_model = None
        
        other_words = list(self.words)
        # M -> number of words:
        M = len(other_words)
        # All words other than current word
        other_words.remove(self.this_word)

        for number_of_states in range(self.min_n_components, self.max_n_components + 1):
            try:
                hmm_model = self.base_model(number_of_states)
                # log(P(X(i)))
                score = hmm_model.score(self.X, self.lengths)

                # SUM(log(P(X(all but i))))
                sum_of_logL_other_than_current_word = 0.0
                for word in other_words:
                    X, lengths = self.hwords[word]
                    sum_of_logL_other_than_current_word += hmm_model.score(X, lengths)

                #DIC
                score = score - (sum_of_logL_other_than_current_word / (M - 1))

                if score > best_score:
                    best_score = score
                    best_model = hmm_model
            except:
                continue

        return best_model
                

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # DONE : implement model selection using CV
        best_score = float('-inf')
        best_model = None

        # DONE : implement model selection using CV
        for n in range(self.min_n_components, self.max_n_components + 1):
            sum_of_logL = 0
            number_of_iterations = 0
            number_of_splits = min(3, len(self.sequences))
            # print(number_of_splits)
            if number_of_splits > 1:
                kfold = KFold(n_splits=number_of_splits)
                for cv_training_set, cv_testing_set in kfold.split(self.sequences):
                    # traning, length_of_training = combine_sequences(cv_training_set, self.sequences)
                    testing, length_of_testing = combine_sequences(cv_testing_set, self.sequences)
                    try:
                        hmm_model = self.base_model(n)
                        logL_score = hmm_model.score(testing, length_of_testing)
                        number_of_iterations = number_of_iterations + 1

                    except:
                        logL_score = 0

                    sum_of_logL = sum_of_logL + logL_score
                
                if number_of_iterations == 0:
                    score = sum_of_logL
                else:
                    score = sum_of_logL / number_of_iterations
            
            else:
                try:
                    hmm_model = self.base_model(n)
                    score = hmm_model.score(self.X, self.lengths)
                except:
                    hmm_model = None
                    score = 0

            if score > best_score:
                best_score = score
                best_model = hmm_model

        return best_model
