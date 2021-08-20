
import cv2
import boto3

bucket = 'panoramic-videos'
date = 17
name = "NVR-CH01_S20210817-000000_E20210817-001334.mp4"
video_path = f"{date}/{name}"
download_path = "/home/videos/{}"
downloaded_file = download_path.format(name)

s3 = boto3.client('s3')
s3.download_file(bucket, video_path, downloaded_file)

cap = cv2.VideoCapture(downloaded_file)


count = 0 

for i in range(999999999):

    ret, frame = cap.read()
    if not ret:
        count = i
        print(count, flush=True)
        cap.release()
        break


print(f"frame count: {count}", flush=True)
