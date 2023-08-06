#!/usr/bin/env python3
# =.- coding: utf-8 -.-

from omic import omic

TEST_USER = '63be793a-6e1b-40cd-9f70-49dd73f470ab'

def setup():
    omic.configure({'user': TEST_USER})

# def test_new_method():
#     return
#     S3_ADDR = 's3://0tmp/1e6271fc9bc9e6c713ac19297c031baf'
#     import boto3
#     import requests
#     # Get the service client.
#     s3 = boto3.client('s3')
#     # Generate the URL to get 'key-name' from 'bucket-name'
#     url = s3.generate_presigned_url(
#         ClientMethod='get_object',
#         Params={
#             'Bucket': '0tmp',
#             'Key': '1e6271fc9bc9e6c713ac19297c031baf'
#         },
#         ExpiresIn=(1 * 60 * 60) # 1 hr
#     )
#     print('url', url)
#     r = requests.get(url, stream=True)
#     with open('testytest', 'wb+') as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             f.write(chunk)

def test_data_public_download():
    setup()
    client = omic.client('data')
    client.download('/', download_dir='test_dl')

def test_data_project_download():
    pass
    # setup()
    # client = omic.client('data')
    # client.download(
    #     vpath='/', 
    #     mode='project',
    #     project='project-48de6638-6a99-40a6-bf2d-dbfa5c158f29',
    #     download_dir='test_dl'
    # )