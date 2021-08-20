
import cv2
import boto3
import sys
sys.stdout.flush()

bucket = 'panoramic-videos'
date = 17
name = "NVR-CH01_S20210817-000000_E20210817-001334.mp4"
video_path = f"{date}/{name}"
download_path = "/home/videos/{}"
downloaded_file = download_path.format(name)

s3 = boto3.client('s3')

print(f"download file: {video_path}")
s3.download_file(bucket, video_path, downloaded_file)

print("cature created")
cap = cv2.VideoCapture(downloaded_file)

count = 0 

print("capture start")
for i in range(999999999):

    ret, frame = cap.read()
    if not ret:
        count = i
        cap.release()
        break
    print(f"count: {i}")


print(f"frame count: {count}")
