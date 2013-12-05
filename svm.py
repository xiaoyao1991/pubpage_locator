from sklearn import svm
from feature_generator import FeatureGenerator
from training_sample_generator import TrainingSampleGenerator
from bclassifier import BaseClassifier
from utils import url_cleanup, get_absolute_url, under_same_maindomain
import urllib2

class SVM(BaseClassifier):
    def __init__(self):
        super(SVM, self).__init__()
    
    def train(self, training_data):
        self.classifier = svm.SVC()
        print training_data[0]
        self.classifier.fit(training_data[0], training_data[1])   # X, Y

        print self.classifier


    def predict(self, lname, root_url):
        pass


if __name__ == '__main__':
    dt = SVM()
    dt.five_fold_test(svm=False, regenerate=False)


