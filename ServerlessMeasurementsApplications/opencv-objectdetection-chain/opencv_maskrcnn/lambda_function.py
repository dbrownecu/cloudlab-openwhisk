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
        trained_model_bucket="maskrcnn-trained"


        weightsPath="frozen_inference_graph.pb"
        configPath = "mask_rcnn_inception_v2_coco_2018_01_28.pbtxt"
        labelsPath = "object_detection_classes_coco.txt"

        local_path = "/tmp/"
        image_path = "/tmp/image.jpeg"

        BUCKET_NAME = record['s3']['bucket']['name']
        S3_KEY = record['s3']['object']['key']

        LABELS = open(local_path+labelsPath).read().strip().split("\n")


        net = cv2.dnn.readNetFromTensorflow(local_path+weightsPath,local_path+configPath)


        image = cv2.imread(image_path)

        blob = cv2.dnn.blobFromImage(image, swapRB=True, crop=False)
        net.setInput(blob)
        boxes = net.forward()


        confidences = []
        classIDs = []

        for i in np.arange(0, boxes.shape[2]):

        	confidence = boxes[0, 0, i, 2]

        	if confidence > confidence_threshold:

        		classID = int(boxes[0, 0, i, 1])
        		confidences.append(float(confidence))
        		classIDs.append(classID)



        print(LABELS[classIDs[0]])


        return {
            "statusCode": 200,
            "body": json.dumps({
                "label": LABELS[classIDs[0]],
            }),
        }
