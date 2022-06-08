import json
import logging

import os
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(SCRIPT_DIR, 'lib')


def lambda_handler(event, context):
    for record in event['Records']:

        import numpy
        import cv2
        confidence_threshold = 0.7
        trained_model_bucket="mobile-net-trained"


        weightsPath="MobileNetSSD_deploy.caffemodel"
        configPath = "MobileNetSSD_deploy.prototxt"

        local_path = "/tmp/"
        image_path = "/tmp/image.jpeg"

        BUCKET_NAME = record['s3']['bucket']['name']
        S3_KEY = record['s3']['object']['key']


        LABELS = ["background", "aeroplane", "bicycle", "bird", "boat",
    	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    	"sofa", "train", "tvmonitor"]


        net = cv2.dnn.readNetFromCaffe(local_path+configPath,local_path+weightsPath)


        image = cv2.imread(image_path)

        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,(300, 300), 127.5)
        net.setInput(blob)
        layerOutputs = net.forward()



        boxes = []
        confidences = []
        classIDs = []

        for i in np.arange(0, layerOutputs.shape[2]):

        	confidence = layerOutputs[0, 0, i, 2]

        	if confidence > confidence_threshold:

        		classID = int(layerOutputs[0, 0, i, 1])
        		confidences.append(float(confidence))
        		classIDs.append(classID)



        print(LABELS[classIDs[0]])


        return {
            "statusCode": 200,
            "body": json.dumps({
                "label": LABELS[classIDs[0]],
            }),
        }
