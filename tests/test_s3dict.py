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
        # sd = self.get_s3dict()
        self.bucket["luke"] = "skywalker"
        self.bucket["obiwan"] = "kenobi"

        self.assertEqual(self.bucket["luke"], "skywalker")
        self.assertEqual(self.bucket["obiwan"], "kenobi")

        del self.bucket["luke"]
        del self.bucket["obiwan"]

        with self.assertRaises(KeyError):
            self.bucket["luke"]

        with self.assertRaises(KeyError):
            self.bucket["obiwan"]

        with self.assertRaises(KeyError):
            self.bucket["x" * 1025] = "X"

    def test_iter(self):
        self.bucket["luke"] = "skywalker"
        self.bucket["obiwan"] = "kenobi"

        keys = []
        for k in self.bucket:
            keys.append(k)

        self.assertEqual(set(keys), set(['luke', 'obiwan']))

    def test_keys(self):
        self.bucket["luke"] = "skywalker"
        self.bucket["obiwan"] = "kenobi"

        keys = []
        for k in self.bucket.keys():
            keys.append(k)

        self.assertEqual(set(keys), set(['luke', 'obiwan']))

    def test_values(self):
        self.bucket["luke"] = "skywalker"
        self.bucket["obiwan"] = "kenobi"

        values = []
        for v in self.bucket.values():
            values.append(v)

        self.assertEqual(set(values), set(['skywalker', 'kenobi']))

    def test_items(self):
        self.bucket["luke"] = "skywalker"
        self.bucket["obiwan"] = "kenobi"

        items = []
        for item in self.bucket.items():
            items.append(item)
        self.assertEqual(set(items), {('luke', 'skywalker'), ('obiwan', 'kenobi')})

    def test_contains(self):
        self.bucket["luke"] = "skywalker"

        self.assertTrue('luke' in self.bucket)
        self.assertTrue('obiwan' not in self.bucket)

    def test_get(self):
        self.assertEqual(self.bucket.get("something", 'not there'), 'not there')
        self.bucket['something'] = 'there'
        self.assertEqual(self.bucket.get("something", 'not there'), 'there')

    def test_clear(self):
        self.bucket["luke"] = "skywalker"
        self.bucket["obiwan"] = "kenobi"

        self.bucket.clear()
        self.assertTrue('luke' not in self.bucket)
        self.assertTrue('obiwan' not in self.bucket)

    def test_clone_to_regular_dict(self):
        d = {}
        self.bucket['luke'] = 'skywalker'
        d['luke'] = 'skywalker'
        self.assertDictEqual(d, dict(self.bucket))

    def test_eq(self):
        self.bucket["luke"] = "skywalker"
        self.bucket["obiwan"] = "kenobi"

        another_bucket = boto3.resource("s3").Bucket('another_bucket')
        another_bucket.create(CreateBucketConfiguration={'LocationConstraint': TEST_REGION_NAME})
        another_bucket["luke"] = "skywalker"
        another_bucket["obiwan"] = "kenobeeeeeeee"
        self.assertNotEqual(self.bucket, another_bucket)

    def test_pop(self):
        self.bucket["a"] = 1
        self.bucket["b"] = 2

        self.assertEqual(self.bucket.pop('a'), 1)
        self.assertEqual(self.bucket.pop('b'), 2)

        with self.assertRaises(KeyError):
            self.bucket.pop('b')

    def test_popitem(self):
        self.bucket["a"] = 1
        self.bucket["b"] = 2

        items = []
        items.append(self.bucket.popitem())
        items.append(self.bucket.popitem())
        self.assertEqual(sorted(items), [('a', 1), ('b', 2)])
        with self.assertRaises(KeyError):
            self.bucket.popitem()

    def test_len(self):
        self.bucket["a"] = 1
        self.bucket["b"] = 2
        self.assertEqual(len(self.bucket), 2)


if __name__ == '__main__':
    unittest.main()
