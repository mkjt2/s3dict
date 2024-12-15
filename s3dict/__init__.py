import pickle
import typing

from typing import Dict

from botocore.exceptions import ClientError
from boto3 import Session


def enable():
    old_session_init = Session.__init__

    def add_custom_method(class_attributes, **kwargs):
        class_attributes['s3dict'] = lambda self: S3Dict(self);

    def new_session_init(self, *args, **kwargs):
        old_session_init(self, *args, **kwargs)
        self.events.register('creating-resource-class.s3.Bucket', add_custom_method)

    Session.__init__ = new_session_init


# TODO update
# TODO setdefault
# TODO README
# TODO packaging

class S3DictValueCodec(typing.Protocol):
    def encode(self, value: typing.Any) -> bytes:
        ...

    def decode(self, data: bytes) -> typing.Any:
        ...


class PickleCodec(S3DictValueCodec):
    def encode(self, value):
        return pickle.dumps(value)

    def decode(self, data):
        return pickle.loads(data)


class S3Dict(Dict):
    def clear(self):
        for k in self:
            del self[k]

    def get(self, item, default=None):
        """ Return the value for key if ky is in the dictionary, else default. """
        try:
            return self[item]
        except KeyError:
            return default

    def items(self):
        # WARNING: this is NOT a dict_keys "view" object.
        for k in self:
            try:
                v = self[k]
            except KeyError:
                continue
            yield k, v

    def keys(self):
        # WARNING: this is NOT a dict_keys "view" object.
        for k in self:
            yield k

    def pop(self, k, *args):
        try:
            v = self[k]
            del self[k]
            return v
        except KeyError:
            if args:
                return args[0]
            raise

    def popitem(self):
        # It's unordered, BTW
        for k in self:
            try:
                return k, self.pop(k)
            except KeyError:
                pass
        raise KeyError("dictionary is empty, cannot popitem")

    def setdefault(self, *args, **kwargs):  # real signature unknown
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        # TODO
        pass

    def update(self, E=None, **F):  # known special case of dict.update
        """
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        """
        # TODO
        pass

    def values(self):
        for k in self.keys():
            try:
                v = self[k]
            except KeyError:
                continue
            yield v

    def __contains__(self, item):
        s3_key = self._validate_item(item)
        try:
            self._s3_client.head_object(Bucket=self._bucket, Key=s3_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise

    def __eq__(self, other):
        if not isinstance(other, S3Dict):
            return False
        for k, v in self.items():
            try:
                other_v = other[k]
                if other_v != v:
                    return False
            except KeyError:
                return False
        for k, v in other.items():
            if k not in self:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def __delitem__(self, item):
        s3_key = self._validate_item(item)
        try:
            self._s3_client.delete_object(Bucket=self._bucket, Key=s3_key)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise KeyError(item)
            else:
                # TODO cover all the error types
                raise RuntimeError("?")

    def __getitem__(self, item):
        try:
            s3_key = self._validate_item(item)
            response = self._s3_client.get_object(Bucket=self._bucket, Key=s3_key)
            s3_content = response['Body'].read()
            return self._codec.decode(s3_content)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise KeyError(item)
            else:
                raise

    def __init__(self, bucket, codec: S3DictValueCodec = PickleCodec()):
        self._bucket = bucket.name
        self._codec = codec
        self._s3_client = bucket.meta.client

    def __iter__(self):
        paginator = self._s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(
                Bucket=self._bucket,
        ):
            for record in page['Contents']:
                yield self._s3_key_to_item(record['Key'])

    def __len__(self, *args, **kwargs):
        result = 0
        for _ in self:
            result += 1
        return result

    def __setitem__(self, item, value):
        s3_content = self._codec.encode(value)
        s3_key = self._validate_item(item)
        self._s3_client.put_object(Bucket=self._bucket, Body=s3_content, Key=s3_key)

    def _validate_item(self, item: str) -> str:
        if type(item) != str:
            raise KeyError('S3 key must be a string')
        if len(item) > 1024:
            raise KeyError('S3 key is too large')
        return item

    def _s3_key_to_item(self, s3_key: str) -> str:
        return s3_key
