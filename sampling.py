
import cv2
import time 
import boto3

bucket = 'panoramic-videos'
date = 17
name = "NVR-CH01_S20210817-000000_E20210817-001334.mp4"
video_path = f"{date}/{name}"

s3 = boto3.client('s3')
s3.download_file(bucket, video_path, f"/home/videos/{name}")



print("download complete")
