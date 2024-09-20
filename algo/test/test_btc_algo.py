import os
from unittest import TestCase, mock
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from algo.btc_algo import data_average, get_job_details

class Test(TestCase):

    @mock.patch.dict(os.environ, {"DIDS": " [ \"8f67E08be5dD941a701c2491E814535522c33bC2\" ]"})
    @mock.patch.dict(os.environ, {"TRANSFORMATION_DID": "6EDaE15f7314dC306BB6C382517D374356E6B9De"})
    @mock.patch.dict(os.environ, {"secret": "MOCK-SECRET"})
    @mock.patch.dict(os.environ, {"ROOT_FOLDER": os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))})
    def test_dataAvg(self):
        print('Testing dataAvg is running')

        data_average(get_job_details())
        # root = os.getenv('ROOT_FOLDER', '')
        # with open(root + '/data/outputs/result.json') as f:
        #     self.assertIsNotNone(f)
