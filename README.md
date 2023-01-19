# Data Engineer Takehome Test

Please clone this repo in your account, send us the link of the solution in your GitHub account together with your application.

## Problem 1:

Build a Python script that detects faces in an image using OpenCV, and saves the headshots of the detected faces to a specified directory. The script should take as input a file path to an image, a directory path to save the headshots, and output the number of faces detected in the image.
Instructions:
- Use OpenCV's Haar Cascade classifier for face detection
- The script should be written in Python and use the following libraries: OpenCV, Numpy, and PIL (Python Imaging Library)
- The script should be well commented and easy to understand
- The script should be able to handle a variety of image types (e.g. jpeg, png, etc.)
- The script should be able to handle images with multiple faces
- The script should save the headshots in the specified directory with the file name in the format "face_1.jpg", "face_2.jpg", etc.


## Solution 1:

- Download the HaarCascade Model Pre-trained by OpenCV to Detect Frontal Face using the following command

```shell
$ wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
```

- These pre-requisites may be required, if you're unable to install PIL
```shell
$ sudo apt-get install libtiff5-dev libjpeg8-dev \
    zlib1g-dev libfreetype6-dev \
    liblcms2-dev libwebp-dev \
    tcl8.6-dev tk8.6-dev python-tk
```

- Install other requirements (it is recommended to use conda or docker)
```shell
$ pip3 install -r requirements.txt
```

- Use the script to detect faces from an image, for example
```
$ python3 face_detect.py -h
    usage: face_detect.py [-h] image-path save-directory

    Detect, crop and save faces from images in a directory

    positional arguments:
      image-path      path to the input image.
      save-directory  path of the directory to save the headshots.

    optional arguments:
      -h, --help      show this help message and exit
```


- Example usage
```shell
$ python3 face_detect.py images/sample.jpg headshots
```

## Problem 2: 

Move all image files from one S3 bucket to another S3 bucket, but only if the image has no transparent pixels.

Objective: Write a Python script that uses the Boto3 library to accomplish the following:

- List all the image files in a given S3 bucket
- Check if each image file has transparent pixels
- If an image file has no transparent pixels, copy it to a different S3 bucket
- If an image file has transparent pixels, log it in a separate file

Guidelines:
- Your script should take the name of the source and destination buckets as input
- You should use the Boto3 library to interact with S3
- You should use the Pillow library to check for transparent pixels in an image
- Your script should handle any errors that may occur during the opening of image file, copy process and anywhere else you deem necessary
- Your script should be well commented and easy to understand
- Your script should be executed from the command line

## Solution 2:

- Install dependencies
```
$ pip3 install -r requirements.txt
```

- Run the script using the command below.
```
$ python3 transfer_learning.py -h

    usage: transfer_images.py [-h]
                              src-bucket dst-bucket aws-access-key-id
                              aws-secret-access-key region

    Transfer images from source bucket to destination bucket using PIL.

    positional arguments:
      src-bucket            Source bucket
      dst-bucket            Destination bucket
      aws-access-key-id     AWS access key id
      aws-secret-access-key AWS Secret access key
      region                Region for the S3 Bucket

    optional arguments:
      -h, --help            show this help message and exit
```