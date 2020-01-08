import unittest
import mock
from lib.testrail_parser import *


class TestTestrailParser(unittest.TestCase):

	def setUp(self):
		pass

	def test_read_csv(self):
		testrail_parser = TestrailParser(['ID', 'Title'])
		testrail_parser.read_csv('./docs/mock_data/mock_testrail_csv_1.csv')
		df = pd.read_csv('./docs/mock_data/mock_testrail_csv_1.csv')
		df = df[['ID', 'Title']]
		df.set_index('ID', drop=True, inplace=True)
		self.assertEqual(testrail_parser.data_frame.to_csv(), df.to_csv())

	def test_get_json(self):
		testrail_parser = TestrailParser(['ID', 'Title'])
		testrail_parser.read_csv('./docs/mock_data/mock_testrail_csv_1.csv')
		except_json = {'C0000': {'Title': '驗證是否能正確登入'}}
		self.assertDictEqual(except_json, testrail_parser.get_json())

	def test_read_two_csv(self):
		testrail_parser = TestrailParser(['ID', 'Title'])
		testrail_parser.read_csv('./docs/mock_data/mock_testrail_csv_1.csv')
		testrail_parser.read_csv('./docs/mock_data/mock_testrail_csv_2.csv')
		except_json = {'C0000': {'Title': '驗證是否能正確登入'}, 'C0001': {'Title': '驗證是否能正確登入'}}
		self.assertDictEqual(except_json, testrail_parser.get_json())



	def tearDown(self):
		pass

if __name__ == '__main__':
    unittest.main()