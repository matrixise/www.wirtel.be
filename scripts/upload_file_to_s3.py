import os
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config


BUCKET_NAME = 'public-mgxio'
FOLDER_NAME = 'wirtel.be'
file_name = 'StephaneWirtel.pdf'

config = Config(
    region_name = 'eu-west-3',
)

s3_client = boto3.client('s3', config=config)

response = s3_client.upload_file(
    os.path.join(os.getcwd(), file_name),
    BUCKET_NAME,
    f'{FOLDER_NAME}/{file_name}',
    ExtraArgs = {'ACL': 'public-read'}
)

