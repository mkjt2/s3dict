#!/usr/bin/env python
from boto3.session import Session
import boto3

from s3dict import S3Dict

aws_access_key_id = 'Cf4thme5jhT8amfWqB0f'
aws_secret_access_key = 'HtGyJ9K4gk15pnNtveQKbwhVPnCnE9ZmUVQgASOg'

def el_reg():
    old_session_init = Session.__init__
    def new_session_init(self, *args, **kwargs):
        old_session_init(self, *args, **kwargs)
        self.events.register('creating-resource-class.s3.Bucket', add_custom_method)
    Session.__init__ = new_session_init

el_reg()


def add_custom_method(class_attributes, **kwargs):
    class_attributes['s3dict'] = lambda self: S3Dict(self);


def main():
    s3 = boto3.resource('s3', endpoint_url='http://localhost:9000', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket = s3.Bucket('test')

    # either bucket must be empty
    # or s3 must have a breadcrumb object that indicates its purpose (s3dict), AND s3dict version
    s3_dict = bucket.s3dict();
    for k, v in s3_dict.items():
        print(k, v);


if __name__ == '__main__':
    main();