import os
import argparse
from tqdm import tqdm
from PIL import Image
from io import BytesIO

class InvalidExtension(Exception):
    pass

class TransparentImage(Exception):
    pass

class UploadFailed(Exception):
    pass

class S3Images:
    """
    S3 images class to read and write Image from S3 bucket
    Reference: https://gist.github.com/ghandic/a48f450f3c011f44d42eea16a0c7014d
    """
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, 
                               aws_secret_access_key=aws_secret_access_key, 
                               region_name=region_name)
        
    def from_s3(self, bucket, key):
        """
        Read image in S3 into PIL Image
        """
        file_byte_string = self.s3.get_object(Bucket=bucket, Key=key)["Body"].read()
        return Image.open(BytesIO(file_byte_string))
    
    def to_s3(self, img, bucket, key):
        """
        Write PIL image to S3 Bucket
        """
        self.__is_transparent_image(img)
        buffer = BytesIO()
        img.save(buffer, self.__get_safe_ext(key))
        buffer.seek(0)
        sent_data = self.s3.put_object(Bucket=bucket, Key=key, Body=buffer)
        if sent_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise UploadFailed(f"Failed to upload image {key} to bucket {bucket}")
        
    def __get_safe_ext(self, key):
        """
        Validate image extension
        """
        ext = os.path.splitext(key)[-1].strip(".").lower()
        if ext in ["jpg", "jpeg"]:
            return "JPEG" 
        elif ext in ["png"]:
            return "PNG" 
        else:
            raise InvalidExtension(f"Invalid extension for image: {key}") 

    def __is_transparent_image(self, img):
        if "transparency" in img.info:
            with open("transparent_images.txt", "a+") as f:
                f.write(image_file + "\n")
            raise TransparentImage(f"Transparent image: {key}") 


def move_images(source_bucket, dest_bucket, aws_access_key_id, aws_secret_access_key, region_name):
    """
    Move images using the S3 Class from one bucket to another.
    """
    # Create an S3Images instance
    images = S3Images(aws_access_key_id, aws_secret_access_key, region_name)
    
    # List all the image files in the source bucket
    result = images.s3.list_objects(Bucket=source_bucket)
    image_files = [content["Key"] for content in result.get("Contents", [])]
    
    if not image_files:
        print("No images found in source bucket")
        return

    # Iterate over the images, 
    # check if it has transparent pixels, 
    # and copy to the destination bucket if it doesn"t
    for image_file in tqdm(image_files):
        try:
            img = images.from_s3(source_bucket, image_file)
            images.to_s3(img, dest_bucket, image_file)
        except InvalidExtension as e:
            print(f"Exception raised: {e}")
        except UploadFailed as e:
            print(f"Exception raised: {e}")
        except TransparentImage as e:
            print(f"Exception raised: {e}")
        except Exception as e:
            print(f"Error while sending image: {e}")
        # Close Open Image
        img.close()
    print(f"Copied all images without transparent pixels to {dest_bucket}")


if __name__ == "__main__":
    # Argument parser for CLI
    parser = argparse.ArgumentParser(description="Transfer images from source bucket to destination bucket using PIL.")
    parser.add_argument("src-bucket", type=str, help="Source bucket")
    parser.add_argument("dst-bucket", type=str, help="Destination bucket")
    parser.add_argument("aws-access-key-id", type=str, help="AWS access key id")
    parser.add_argument("aws-secret-access-key", type=str, help="AWS Secret access key")
    parser.add_argument("region", type=str, help="Region for the S3 Bucket")

    # Parse args and Transfer Images!
    args = parser.parse_args()
    move_images(args.src_bucket, args.dst_bucket, args.aws_access_key_id, args.aws_secret_access_key, args.region_name)

