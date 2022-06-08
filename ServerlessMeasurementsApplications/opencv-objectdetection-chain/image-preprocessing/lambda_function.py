
import os
import sys
import uuid
import cv2
from urllib.parse import unquote_plus


# from PIL import Image
# import PIL.Image


# def resize_image(image_path, resized_path):
#     with Image.open(image_path) as image:
#         image.thumbnail(tuple(x / 2 for x in image.size))
#         image.save(resized_path)

def preprocess_image(download_path, upload_path):
    img = cv2.imread(download_path)
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imwrite(upload_path,img)

def lambda_handler(event, context):
    classification_bucket_1 = 'fanout-trigger-maskrcnn'
    classification_bucket_2 = 'fanout-trigger-yolo'
    classification_bucket_3 = 'fanout-trigger-mobilenet'
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)

        preprocess_image(download_path, upload_path)
        #s3_client.upload_file(upload_path, '{}-resized'.format(bucket), key)

        #comment below


        s3_client.upload_file(upload_path,classification_bucket_1, key)
        s3_client.upload_file(upload_path,classification_bucket_2, key)
        s3_client.upload_file(upload_path,classification_bucket_3, key)
