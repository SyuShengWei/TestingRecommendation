from lib.testrail_parser import TestrailParser

class TestingRecommender():

    def __init__(self):
    	self.data = None

    def preprocess(self, preprocessor_list):
    	for preprocessor in preprocessor_list:
    		self.data = preprocessor.preprocessing(self.data)