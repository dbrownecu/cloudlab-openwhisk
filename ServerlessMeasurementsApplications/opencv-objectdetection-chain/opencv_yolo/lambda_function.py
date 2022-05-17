import json
import logging
import boto3
import botocore
import os
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'lib')

def downloadFromS3(strBucket,strKey,strFile):
    print(strBucket,strKey,strFile)
    s3_client = boto3.client('s3')
    #s3_client.download_file(strBucket, strKey, strFile)
    s3 = boto3.resource('s3')
    s3.Bucket(strBucket).download_file(strKey, strFile)

def lambda_handler(event, context):
    for record in event['Records']:

        import numpy
        import cv2
        confidence_threshold = 0.7
        trained_model_bucket="yolo-trained"
        coco_names = "coco.names"
        cfg = "yolov3.cfg"
        weights = "yolov3.weights"
        yolo_path = "/tmp/"
        image_path = "/tmp/image.jpeg"

        BUCKET_NAME = record['s3']['bucket']['name']
        S3_KEY = record['s3']['object']['key']


        downloadFromS3(trained_model_bucket,coco_names,yolo_path+coco_names)
        downloadFromS3(trained_model_bucket,cfg,str(yolo_path+cfg))
        downloadFromS3(trained_model_bucket,weights,yolo_path+weights)
        downloadFromS3(BUCKET_NAME,S3_KEY,image_path)

        labelsPath = os.path.sep.join([yolo_path, "coco.names"])
        LABELS = open(yolo_path+coco_names).read().strip().split("\n")


        weightsPath = os.path.sep.join([yolo_path, "yolov3.weights"])
        configPath = os.path.sep.join([yolo_path, "yolov3.cfg"])
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


        image = cv2.imread(image_path)
        (H, W) = image.shape[:2]
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
        net.setInput(blob)

        layerOutputs = net.forward(ln)

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:

        	for detection in output:
        	    scores = detection[5:]
        	    classID = np.argmax(scores)
        	    confidence = scores[classID]
        	    if confidence > confidence_threshold:
        	        confidences.append(float(confidence))
        	        classIDs.append(classID)

        print(LABELS[classIDs[0]])


        return {
            "statusCode": 200,
            "body": json.dumps({
                "label": LABELS[classIDs[0]],
            }),
        }
