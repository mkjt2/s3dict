from s3dict import S3Dict
import os

os.environ['AWS_ACCESS_KEY_ID'] = 'g48ShmmaEtuyQvopD2p7'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'wWhCbWHvGhqgn1XrN0trDIgASYwwvV4bwNzrjSkg'


s = S3Dict()
print(s["xfinity_sept.pdf"])
