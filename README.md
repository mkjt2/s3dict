# S3Dict - Access S3 buckets as dictionaries

## Install

    pip install s3dict

## Usage

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

## Why oh why?

Just for curiosity. `bucket[k] = v` is easier than `bucket.put_object(Key=k, Body=pickle.dumps(v))` right? :)

Please let us know if you found a real use case.

## Limitations

- Buckets are not ordered like Python dictionaries are ordered (by insertion order).
- `len(bucket)` runs O(N) - it lists bucket objects and counts.
- `popitem()` returns an arbitrary item (since unordered).
- `keys()` and `values()` are iterators, not [views](https://www.codeguage.com/courses/python/dictionaries-views).
- Dictionary keys must be `str`. They cannot be too long (underlying S3 key may not be >1024 chars).
- Dictionary values must be serializable (Pickle by default, you can bring your own serialization / "codec").

## Contributions

They are welcome. TODOs offers some ideas.