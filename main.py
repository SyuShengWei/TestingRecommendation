import os

from lib.testrail_parser import TestrailParser
from lib.testing_recommender import TestingRecommender
from lib.json_preprocessor import JsonPreprocessorLanguageTranslator as LT

TESTRAIL_EXPORTED_CSV_FOLDER = './docs/raw_data'


if __name__ == '__main__':
    referenece_field = ['ID', # the first column should be the index
                        'Title',
                        'Expected Result',
                        'Preconditions',
                        'Section Hierarchy',
                        'Steps.1',
                        'Suite',
                        'Test purpose',
                        ]
    
    ## Read testrail csv file and parse them into json
    testrail_parser = TestrailParser(referenece_field)
    for file_name in os.listdir(TESTRAIL_EXPORTED_CSV_FOLDER):
    	file_name = 'tis.csv'
    	csv_file_path = os.path.join(TESTRAIL_EXPORTED_CSV_FOLDER,file_name)
    	testrail_parser.read_csv(csv_file_path)
    	break

    json_data = testrail_parser.get_json()
    print(len(json_data.keys()))
    for k in json_data:
    	print(k, json_data[k])
    	break

    testing_recommender = TestingRecommender()
    print('-======processor')
    processor = LT('zh-CN', 'en')
    processor.preprocessing(json_data)

    print(len(json_data.keys()))
    for k in json_data:
    	print(k, json_data[k])
    	break


    disambiguation_dict = {
    	'sw': 'switching'
    	'serviceswitching': 'swithcing'
    	'txadapter': 'transaction adapter'
    	'adapter': 'transcation adapter'
    	'transactionadapter': 'transcation adapter'
    	'minitis': 'mini tis'
    	'miniswitching': 'mini switching'
    	'minisw': 'mini switching'
    }