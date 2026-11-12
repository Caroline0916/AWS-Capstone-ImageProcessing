# Serverless Image Processing Pipeline

**Course:** CCMP200 – Cloud Computing  
**Project:** AWS Capstone Project  
**Student:** Caroline Aneya

## 1. Project Overview

This project implements a serverless image processing pipeline using Amazon Web Services (AWS). It automatically resizes uploaded images into thumbnails using AWS Lambda and stores the processed images in a separate Amazon S3 bucket.

The project also provides an API Gateway endpoint that starts an AWS Step Functions workflow to process images.

## 2. AWS Services Used

- **Amazon S3:** Stores original images and resized thumbnails.
- **AWS Lambda:** Processes and resizes images using Python and Pillow.
- **AWS Step Functions:** Coordinates image processing, checks the Lambda result, and handles success or failure.
- **Amazon API Gateway:** Provides a REST API endpoint to initiate the Step Functions workflow.
- **AWS IAM:** Controls permissions between AWS services.
- **Amazon CloudWatch:** Provides logs for troubleshooting and monitoring.

## 3. System Architecture

**Automatic S3 Upload Processing:**

Original S3 Bucket → S3 Event Notification → AWS Lambda → Resized S3 Bucket

**API-Based Processing:**

API Gateway → Step Functions → AWS Lambda → Resized S3 Bucket

Both processing paths use the same Lambda function.

## 4. Project Components

**Original S3 Bucket:** `capstone-original-images-513134`

**Resized S3 Bucket:** `capstone-resized-images-513134`

**Lambda Function:** `ResizeImageFunction`

**Step Functions State Machine:** `ImageProcessingStateMachine`

**API Gateway:** `ImageProcessingAPI`

**API Endpoint:** `POST /resize`

## 5. How the Application Works

1. A PNG image is uploaded to the original S3 bucket.
2. An S3 event notification automatically invokes the Lambda function.
3. The Lambda function downloads the image from S3.
4. Python Pillow resizes the image to fit within 200 × 200 pixels while maintaining its aspect ratio.
5. The resized image is converted to JPEG format.
6. The thumbnail is saved in the resized S3 bucket with `_thumbnail.jpg` added to its filename.

Alternatively, an API request can start the Step Functions workflow. The workflow invokes Lambda, evaluates the returned processing status, and transitions to either a success or failure state.

## 6. Testing and Results

The following tests were completed successfully:

- Lambda function invoked with a test event.
- Original image processed and resized.
- Thumbnail generated in the destination S3 bucket.
- Step Functions execution completed successfully.
- API Gateway POST request returned HTTP 200 with an execution ARN.
- Uploading a new PNG image automatically triggered Lambda and generated a thumbnail.

## 7. Source Code

- `lambda_function.py` — Python image resizing function.
- `step-functions.json` — AWS Step Functions workflow definition.
- `README.md` — Project documentation.

## 8. Conclusion

The AWS Serverless Image Processing Pipeline demonstrates event-driven processing, serverless computing, workflow orchestration, API integration, and cloud storage. Testing confirmed that the application can process images through both S3 event notifications and an API-initiated Step Functions workflow.