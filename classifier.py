from sklearn import tree
from feature_generator import FeatureGenerator
from training_sample_generator import TrainingSampleGenerator
from queue import Queue
from utils import url_cleanup, get_absolute_url, under_same_maindomain
import urllib2
from bs4 import BeautifulSoup

class DecisionTree(object):
    def __init__(self):
        super(DecisionTree, self).__init__()
        self.feature_generator = FeatureGenerator()
        self.tree = None 


    
    def train(self, training_data):
        self.tree = tree.DecisionTreeClassifier()
        self.tree.fit(training_data[0], training_data[1])   # X, Y

    def inference(self, testing_data, verbose=True):
        count_correct = 0
        count_wrong = 0
        for vector_label_pair in testing_data:
            predicted_result = self.tree.predict(vector_label_pair[0])
            if predicted_result[0] == vector_label_pair[1]:
                count_correct += 1
            else:
                count_wrong += 1

        if verbose:
            print 'Correctly labeled: ', count_correct
            print 'Wrong labeled: ', count_wrong


    def predict(self, lname, root_url):
        pass


    

    def five_fold_test(self, path):
        tsg = TrainingSampleGenerator()
        # tsg.generate(path)
        # tsg.serialize()
        tsg.deserialze()
        five_folds = tsg.five_folds()

        for fold in five_folds:
            training_data_wrapper= ([vector_label_pair[0] for vector_label_pair in fold[0]], [vector_label_pair[1] for vector_label_pair in fold[0]])
            self.train(training_data_wrapper)
            self.inference(fold[1])





if __name__ == '__main__':
    dt = DecisionTree()
    dt.train('sample.txt')


