from data import Data
from feature_generator import FeatureGenerator
from queue import Queue
from utils import url_cleanup, get_absolute_url, under_same_maindomain
import urllib2
from bs4 import BeautifulSoup
import pickle

class TrainingSampleGenerator(object):
    def __init__(self, svm_feature=False):
        super(TrainingSampleGenerator, self).__init__()
        self.training_samples = []
        self.processed_training_data = []   # format: tuple([feature vector] , label)
        self.feature_generator = FeatureGenerator()
        self.svm_feature = svm_feature

    def parse_from_text(self, path):
        fp = open(path, 'r')
        counter = 0
        lname = None
        root_url = None
        target_url = None

        for line in fp:
            counter += 1
            if counter == 4:
                data = Data(lname, root_url, target_url)
                self.training_samples.append(data)
                counter = 0
                continue

            elif counter == 1:
                lname = line.lower().strip()
            elif counter == 2:
                root_url = line.strip()
            elif counter == 3:
                target_url = line.strip()


    def generate(self, path):   # process and generate training data
        self.parse_from_text(path)

        for raw_training_data in self.training_samples:
            self.processed_training_data +=  self.convert_raw_training_data_to_features(raw_training_data)

        print self.processed_training_data


    def serialize(self):
        fp = open('processed_training_data.pkl', 'wb')
        pickle.dump(self.processed_training_data, fp)
        fp.close()

    def deserialize(self):
        self.processed_training_data = pickle.load(open('processed_training_data.pkl', 'rb'))


    def convert_raw_training_data_to_features(self, train_data):
        q = Queue()
        url_deduplicator = {}
        DELIMITER = ('###DELIMITER###', '', -1)

        lname = train_data.lname
        root_url = train_data.root_url
        target_url = train_data.target_url
        self.feature_generator.setup(lname, root_url)

        training_data_features = []

        q.push( (root_url, '', 0) )
        q.push(DELIMITER)
        level_count = 0
        stop_pushing_flag = False

        while not q.is_empty():
            cur_url_info = q.pop()
            print cur_url_info
            print target_url, len(target_url)

            if cur_url_info == DELIMITER:   #if delimiter, increment level counter
                level_count += 1
                if level_count == 1:     #dig no mare than 1 levels
                    stop_pushing_flag = True
                else:
                    continue

            if url_deduplicator.has_key(url_cleanup(cur_url_info[0])):  # if appeared, ignore
                continue
            else:
                url_deduplicator[url_cleanup(cur_url_info[0])] = True

            self.feature_generator.generate_features(cur_url_info, self.svm_feature)

            if self.feature_generator.features:     #if feautures is [], then means previous is an invalid link
                if url_cleanup(cur_url_info[0]) == target_url:
                    training_data_features.append( (self.feature_generator.features, 1) )
                    print '\t\t', (self.feature_generator.features, 1)
                else:
                    training_data_features.append( (self.feature_generator.features, 0) )
                    print '\t\t', (self.feature_generator.features, 0)

                # Push sublinks
                if not stop_pushing_flag:
                    try:
                        raw_html = urllib2.urlopen(cur_url_info[0], timeout=3).read()
                        soup = BeautifulSoup(raw_html)
                        a_lst = soup.find_all('a', href=True)
                        for anchor in a_lst:
                            # new_url = urllib2.urlparse.urljoin(cur_url_info[0], anchor.attrs['href'])
                            new_url = get_absolute_url(cur_url_info[0], anchor.attrs['href'])
                            if under_same_maindomain(cur_url_info[0], new_url):
                                q.push( (new_url, anchor.text, level_count+1) )
                        if cur_url_info[2] == 0:
                            q.push(DELIMITER)
                    except:
                        pass

        self.feature_generator.close_up()
        return training_data_features



    def five_folds(self):
        """
            Format:
                [
                    (
                        [([feature vector], label), (), ...],     #training set 80%     fold[0]
                        [([feature vector], label), (), ...]      #testing set 20%      fold[1]
                    )  #1st fold,
                    
                    ()....
                ]
        """
        total_len = len(self.processed_training_data)
        five_folds = []
        test_set_len = total_len - 4 * (total_len/5)

        print 'total len: ', total_len

        for i in xrange(5):
            test_set = []
            for j in xrange(test_set_len):
                idx = i * (total_len/5) + j
                test_set.append(self.processed_training_data[idx])
            training_set = self.processed_training_data[: i*(total_len/5)] + self.processed_training_data[i*(total_len/5) + test_set_len :]
            five_folds.append( (training_set, test_set) )

        return five_folds


if __name__ == '__main__':
    tsg = TrainingSampleGenerator()
    # tsg.generate('sample.txt')
    # tsg.serialize()
    tsg.deserialize()
    print tsg.five_folds()