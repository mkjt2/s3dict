


def main():
    import boto3
    import s3dict
    s3dict.enable()

    # create a boto3 bucket resource
    bucket = boto3.resource("s3").Bucket('s3dict-test')

    # S3 object with key 'hello' is created, with content 'world' (pickled)
    bucket['hello'] = 'world'
    bucket['hola'] = 'mundo'

    for k, v in bucket.items():
        print(f'{k} -> {v}')

    del bucket['hello']

if __name__ == '__main__':
    main()
