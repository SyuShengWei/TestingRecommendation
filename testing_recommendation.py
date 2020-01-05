from lib.testrail_parser import TestrailParser

class TestingRecommender():

    def __init__(self):
        pass

    def read_testrail_csv_from_docs(self, referenced_field: list()) -> dict:
    """
    This function is used to read data from docs/
    Parameters:
        referenced_field: a list of string, each element is the field name of csv.
                          every field which is used to count the simulariy should in this list
    Depandancy Docs:
        the export files of testrail with all detail.
        the file shoud be put in raw_data/
    """



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
    testing_recommender = TestingRecommender()
    testing_recommender.read_testrail_csv_from_docs()