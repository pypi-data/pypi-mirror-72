# Result from response = requests.post('.../ingest/upload/')

# response.content
content = b'{"data":"https://amazons3/storage/Ceph.S3_29-Apr-2020_WIHEFeX.csv?AWSAccessKeyId=KJJL9UBPFGGV85M9MHOB&Signature=0LxHBMQfDrMUSSqAqkJFVTIm08U%3D&Expires=1592112220"}'

# response.json()
json = {'data': 'https://amazons3/storage/Ceph.S3_29-Apr-2020_WIHEFeX.csv?AWSAccessKeyId=KJJL9UBPFGGV85M9MHOB&Signature=0LxHBMQfDrMUSSqAqkJFVTIm08U%3D&Expires=1592112220'}
