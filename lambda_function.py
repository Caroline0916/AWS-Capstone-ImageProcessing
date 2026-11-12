import boto3
import os
import io
from urllib.parse import unquote_plus
from PIL import Image

s3 = boto3.client("s3")
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]

def lambda_handler(event, context):
    try:
        # Accept input from S3 triggers or Step Functions
        if "Records" in event:
            record = event["Records"][0]
            source_bucket = record["s3"]["bucket"]["name"]
            image_key = unquote_plus(
                record["s3"]["object"]["key"]
            )
        else:
            source_bucket = event["bucket"]
            image_key = event["key"]

        # Download original image from S3
        response = s3.get_object(
            Bucket=source_bucket,
            Key=image_key
        )
        image_data = response["Body"].read()

        # Resize image to thumbnail
        with Image.open(io.BytesIO(image_data)) as image:
            image.thumbnail((200, 200))

            # Convert to RGB for JPEG output
            if image.mode != "RGB":
                image = image.convert("RGB")

            output = io.BytesIO()
            image.save(output, format="JPEG")
            output.seek(0)

        # Create thumbnail filename
        filename = os.path.splitext(image_key)[0]
        output_key = filename + "_thumbnail.jpg"

        # Save thumbnail to resized-images bucket
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=output.getvalue(),
            ContentType="image/jpeg"
        )

        return {
            "status": "success",
            "output_bucket": OUTPUT_BUCKET,
            "output_key": output_key
        }

    except Exception as e:
        print(f"Error processing image: {str(e)}")

        return {
            "status": "failed",
            "error": str(e)
        }
