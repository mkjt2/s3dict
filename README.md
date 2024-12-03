# S3Dict - Distributed Python dictionary backed by S3

## Install

    pip install s3dict

## Basic Usage

    from s3dict import S3Dict

    # create a boto3 s3 client
    s3_client = boto3.client('s3', region_name='us-west-2')

    # prepare a bucket that you can read / write on
    bucket = 's3-dict-bucket'

    # configure S3Dict. All S3Dict instances will use these configuration
    S3Dict.configure(s3_client, bucket)
    
    # create and use S3Dict's
    sd = S3Dict()
    sd['hello'] = 'world'
    del sd['hello']

    for k, v in sd.items():
        print(f'{k} {v}')

## Distributed mode

S3Dict stores data in an S3 bucket. A single S3 bucket can contain multiple S3Dict's.

Each S3Dict has a unique `dict_id`. A S3Dict may be accessed from different processes by:

- Configuring the same common S3 bucket.
- Referencing the same `dict_id`.

From process A:

    sd = S3Dict()
    sd["quote"] = "say hello"
    print(sd.dict_id)
    # "<SOME_UUID>"

From process B:

    sd = S3Dict.open("<SOME_UUID>")
    sd["quote"] += " to my little friend"

From process A & B:

    print(sd["quote"])
    # "say hello to my little friend"

## Listing S3Dict's in a bucket

    S3Dict.dict_ids()

## Deleting an S3Dict from a bucket
    
    S3Dict.purge(dict_id)

## Operations mapping

TODO: table of dict ops to s3 ops

## Limitations and caveats

- S3Dict's are unordered.
- `len(s3dict)` runs in O(N) - it lists objects in S3 and does a count.
- `popitem()` will operate on an arbitrary item (since unordered).
- `keys()` and `values()` are basic iterators, not views.
- Dictionary keys must be `str`. They cannot be too long (underlying S3 key may not be >1024 chars).
- 