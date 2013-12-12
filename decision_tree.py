from sklearn import tree
from feature_generator import FeatureGenerator
from training_sample_generator import TrainingSampleGenerator
from bclassifier import BaseClassifier
from utils import url_cleanup, get_absolute_url, under_same_maindomain
import urllib2
from sklearn.externals.six import StringIO  
import pydot 

class DecisionTree(BaseClassifier):
    def __init__(self):
        super(DecisionTree, self).__init__()
        self.classifier = tree.DecisionTreeClassifier()
    
    def train(self, training_data):
        self.classifier.fit(training_data[0], training_data[1])   # X, Y


    def predict(self, lname, root_url):
        pass


if __name__ == '__main__':
    dt = DecisionTree()
    dt.five_fold_test()
    print dt.classifier

    # Print tree
    # dot_data = StringIO() 
    # tree.export_graphviz(dt.classifier, out_file=dot_data) 
    # graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
    # graph.write_pdf("dt.pdf") 
