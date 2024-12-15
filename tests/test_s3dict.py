import unittest
import boto3
import s3dict
s3dict.enable()
from moto import mock_aws

TEST_BUCKET_NAME = "test"
TEST_REGION_NAME = "us-west-2"
S3_CLIENT = boto3.client('s3', region_name=TEST_REGION_NAME)


class TestS3Dict(unittest.TestCase):
    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()
        self.bucket = boto3.resource("s3").Bucket(TEST_BUCKET_NAME)
        self.bucket.create(CreateBucketConfiguration={'LocationConstraint': TEST_REGION_NAME})

    def tearDown(self):
        self.mock_aws.stop()

    def get_s3dict(self):
        return self.bucket.s3dict()

    def test_set_get_del_cycle(self):
        sd = self.get_s3dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        self.assertEqual(sd["luke"], "skywalker")
        self.assertEqual(sd["obiwan"], "kenobi")

        del sd["luke"]
        del sd["obiwan"]

        with self.assertRaises(KeyError):
            sd["luke"]

        with self.assertRaises(KeyError):
            sd["obiwan"]

        with self.assertRaises(KeyError):
            sd["x" * 1025] = "X"

    def test_iter(self):
        sd = self.get_s3dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        keys = []
        for k in sd:
            keys.append(k)

        self.assertEqual(set(keys), set(['luke', 'obiwan']))

    def test_keys(self):
        sd = self.get_s3dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        keys = []
        for k in sd.keys():
            keys.append(k)

        self.assertEqual(set(keys), set(['luke', 'obiwan']))

    def test_values(self):
        sd = self.get_s3dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        values = []
        for v in sd.values():
            values.append(v)

        self.assertEqual(set(values), set(['skywalker', 'kenobi']))

    def test_items(self):
        sd = self.get_s3dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        items = []
        for item in sd.items():
            items.append(item)
        self.assertEqual(set(items), {('luke', 'skywalker'), ('obiwan', 'kenobi')})

    def test_contains(self):
        sd = self.get_s3dict()
        sd["luke"] = "skywalker"

        self.assertTrue('luke' in sd)
        self.assertTrue('obiwan' not in sd)

    def test_get(self):
        sd = self.get_s3dict()
        self.assertEqual(sd.get("something", 'not there'), 'not there')
        sd['something'] = 'there'
        self.assertEqual(sd.get("something", 'not there'), 'there')

    def test_clear(self):
        sd = self.get_s3dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        sd.clear()
        self.assertTrue('luke' not in sd)
        self.assertTrue('obiwan' not in sd)

    def test_clone_to_regular_dict(self):
        sd = self.get_s3dict()
        d = {}
        sd['luke'] = 'skywalker'
        d['luke'] = 'skywalker'
        self.assertDictEqual(d, dict(sd))

    def test_eq(self):
        sd1 = self.get_s3dict()
        sd1["luke"] = "skywalker"
        sd1["obiwan"] = "kenobi"

        another_bucket = boto3.resource("s3").Bucket('another_bucket')
        another_bucket.create(CreateBucketConfiguration={'LocationConstraint': TEST_REGION_NAME})
        sd2 = another_bucket.s3dict()
        sd2["luke"] = "skywalker"
        sd2["obiwan"] = "kenobeeeeeeee"
        self.assertNotEqual(sd1, sd2)

    def test_pop(self):
        sd = self.get_s3dict()
        sd["a"] = 1
        sd["b"] = 2

        self.assertEqual(sd.pop('a'), 1)
        self.assertEqual(sd.pop('b'), 2)

        with self.assertRaises(KeyError):
            sd.pop('b')

    def test_popitem(self):
        sd = self.get_s3dict()
        sd["a"] = 1
        sd["b"] = 2

        items = []
        items.append(sd.popitem())
        items.append(sd.popitem())
        self.assertEqual(sorted(items), [('a', 1), ('b', 2)])
        with self.assertRaises(KeyError):
            sd.popitem()

    def test_len(self):
        sd = self.get_s3dict()
        sd["a"] = 1
        sd["b"] = 2
        self.assertEqual(len(sd), 2)


if __name__ == '__main__':
    unittest.main()
