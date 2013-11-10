from utils import is_valid_url
from builtin_features import *

class FeatureGenerator(object):
    def __init__(self):
        super(FeatureGenerator, self).__init__()
        self.features = []
        self.pipeline = []
        self.lname = None
        self.root_url = None


    def add_feature(self, cls):
        self.pipeline.append(cls(self.lname, self.root_url))

    def setup(self, lname, root_url):
        self.lname = lname
        self.root_url = root_url
        
        if not self.pipeline:
            self.add_feature(IsRootURLFeature)
            self.add_feature(IsFirstLevelSublinkFeature)
            # self.add_feature(IsSecondLevelSublinkFeature)
            # self.add_feature(IsUnderSameDomainFeature)
            self.add_feature(URLAnchorTextHasKeywordsFeature)
            self.add_feature(URLHasKeywordsFeature)
            self.add_feature(URLHasLnameFeature)
            self.add_feature(HasKeywordsFeature)
            self.add_feature(TitleHasKeywordsFeature)
            self.add_feature(HasLnameMoreThanKTimesFeature)
            self.add_feature(HasRecurringPatternFeature)
            self.add_feature(HasConsecutivePDFOutlinksFeature)
            self.add_feature(HasManyBookmarkLinkFeature)


    def generate_features(self, url_info):
        # preprocess the url_info
        self.features = []
        if is_valid_url(url_info[0]):
            print url_info[0], len(url_info[0])
            for feature_obj in self.pipeline:
                self.features.append( feature_obj.extract(url_info) )
        else:
            self.features = []

    # def generate_features(self, url_info):
    #     # preprocess the url_info
    #     if is_valid_url(url_info[0]):
    #         for feature_obj in self.pipeline:
    #             self.features.append(feature_obj.extract(url_info)
    #     else:
    #         self.features = []