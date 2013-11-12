from feature_generator import FeatureGenerator
from training_sample_generator import TrainingSampleGenerator

class BaseClassifier(object):
    def __init__(self):
        super(BaseClassifier, self).__init__()
        self.feature_generator = FeatureGenerator()
        self.classifier = None 

    def train(self, training_data):
        raise NotImplementedError("Not Implemented!")


    def predict(self, lname, root_url):
        raise NotImplementedError("Not Implemented!")

    
    def inference(self, testing_data, verbose=True):
        count_correct = 0
        count_wrong = 0
        for vector_label_pair in testing_data:
            predicted_result = self.classifier.predict(vector_label_pair[0])
            print 'predicted: ', predicted_result[0], '\treal: ', vector_label_pair[1] 
            if predicted_result[0] == vector_label_pair[1]:
                count_correct += 1
            else:
                count_wrong += 1
                print '\tWRONG!!!!!'

        if verbose:
            print 'Correctly labeled: ', count_correct
            print 'Wrong labeled: ', count_wrong




    def five_fold_test(self):
        tsg = TrainingSampleGenerator()
        # tsg.generate(path)
        # tsg.serialize()
        tsg.deserialize()
        five_folds = tsg.five_folds()

        for fold in five_folds:
            # wrap the data into fittable data format
            training_data_wrapper= ([vector_label_pair[0] for vector_label_pair in fold[0]], [vector_label_pair[1] for vector_label_pair in fold[0]])
            self.train(training_data_wrapper)
            self.inference(fold[1])
