import unittest
import boto3
from moto import mock_aws

from s3dict import S3Dict

TEST_BUCKET_NAME = "test"
TEST_REGION_NAME = "us-west-2"
S3_CLIENT = boto3.client('s3', region_name=TEST_REGION_NAME)
S3Dict.configure(S3_CLIENT, TEST_BUCKET_NAME)


class TestS3Dict(unittest.TestCase):
    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()
        S3_CLIENT.create_bucket(Bucket=TEST_BUCKET_NAME,
                                CreateBucketConfiguration={"LocationConstraint": TEST_REGION_NAME})

    def tearDown(self):
        self.mock_aws.stop()

    def test_purge(self):
        """ TODO """

    def test_dict_ids(self):
        """ TODO """

    def test_set_get_del_cycle(self):
        sd = S3Dict()
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

    def test_iter(self):
        sd = S3Dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        keys = []
        for k in sd:
            keys.append(k)

        self.assertEqual(keys, ['luke', 'obiwan'])

    def test_keys(self):
        sd = S3Dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        keys = []
        for k in sd.keys():
            keys.append(k)

        self.assertEqual(keys, ['luke', 'obiwan'])

    def test_values(self):
        sd = S3Dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        values = []
        for v in sd.values():
            values.append(v)

        self.assertEqual(values, ['skywalker', 'kenobi'])

    def test_items(self):
        sd = S3Dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        items = []
        for item in sd.items():
            items.append(item)
        self.assertEqual(items, [('luke', 'skywalker'), ('obiwan', 'kenobi')])

    def test_contains(self):
        sd = S3Dict()
        sd["luke"] = "skywalker"

        self.assertTrue('luke' in sd)
        self.assertTrue('obiwan' not in sd)

    def test_get(self):
        sd = S3Dict()
        self.assertEqual(sd.get("something", 'not there'), 'not there')
        sd['something'] = 'there'
        self.assertEqual(sd.get("something", 'not there'), 'there')

    def test_clear(self):
        sd = S3Dict()
        sd["luke"] = "skywalker"
        sd["obiwan"] = "kenobi"

        sd.clear()
        self.assertTrue('luke' not in sd)
        self.assertTrue('obiwan' not in sd)

    def test_clone_to_regular_dict(self):
        sd = S3Dict()
        d = {}
        sd['luke'] = 'skywalker'
        d['luke'] = 'skywalker'
        self.assertDictEqual(d, dict(sd))

    def test_eq(self):
        sd1 = S3Dict()
        sd1["luke"] = "skywalker"
        sd1["obiwan"] = "kenobi"

        sd2 = S3Dict()
        sd2["luke"] = "skywalker"
        sd2["obiwan"] = "kenobeeeeeeee"
        self.assertNotEqual(sd1, sd2)

    def test_copy(self):
        sd1 = S3Dict()
        sd1["luke"] = "skywalker"
        sd1["obiwan"] = "kenobi"

        sd2 = sd1.copy()

        self.assertEqual(sd1, sd2)

        sd2["darth"] = "vader"
        self.assertNotEqual(sd1, sd2)

    def test_from_keys(self):
        sd = S3Dict.fromkeys(["k1", "k2"], value=None)
        self.assertEqual(dict(sd), {'k1': None, 'k2': None})

    def test_pop(self):
        sd = S3Dict()
        sd["a"] = 1
        sd["b"] = 2

        self.assertEqual(sd.pop('a'), 1)
        self.assertEqual(sd.pop('b'), 2)

        with self.assertRaises(KeyError):
            sd.pop('b')

    def test_popitem(self):
        sd = S3Dict()
        sd["a"] = 1
        sd["b"] = 2

        items = []
        items.append(sd.popitem())
        items.append(sd.popitem())
        self.assertEqual(sorted(items), [('a', 1), ('b', 2)])
        with self.assertRaises(KeyError):
            sd.popitem()

    def test_len(self):
        sd = S3Dict()
        sd["a"] = 1
        sd["b"] = 2
        self.assertEqual(len(sd), 2)

    def test_open(self):
        sd1 = S3Dict()

        sd2 = S3Dict.open(sd1.dict_id)

        sd1['a'] = 1
        self.assertEqual(sd2['a'], 1)


if __name__ == '__main__':
    unittest.main()
