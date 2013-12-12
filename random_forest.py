from sklearn.ensemble import RandomForestClassifier
from feature_generator import FeatureGenerator
from training_sample_generator import TrainingSampleGenerator
from bclassifier import BaseClassifier

class RandomForest(BaseClassifier):
    def __init__(self, n_estimators=1000, criterion='gini', max_depth=None):
        super(RandomForest, self).__init__()
        self.classifier = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth)
    
    def train(self, training_data):
        self.classifier.fit(training_data[0], training_data[1])   # X, Y


    def predict(self, lname, root_url):
        pass


if __name__ == '__main__':
    dt = RandomForest()
    dt.five_fold_test()