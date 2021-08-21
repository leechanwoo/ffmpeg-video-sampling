
import cv2
import boto3
import sys
sys.stdout.flush()

s3 = boto3.client('s3')
name = "NVR-CH01_S20210817-000000_E20210817-001334.mp4"
out_name = "out_" + name


out_path = f"test/{out_name}"
out_bucket = 'extracted-panoramic-images'
s3.upload_file(out_name, out_bucket, out_path)

exit()
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
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

out_name = "out_" + name
frameSize = (int(width/4), int(height/4))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(out_name, fourcc, fps, frameSize)

print(f"org length: {length}")
print(f"org fps: {fps}")
print(f"org dimension: {width}, {height}")
print(f"out dimension: {width/4}, {height/4}")
print(f"out fps: fps")

print("capture start")
n = 20
samples_interval = length/n

for i in range(100):
    ret, frame = cap.read()
    if not ret:
        cap.release()
        writer.release()
        break

    progress = int(i/length*100)
    print(f"{i}/{length} {progress}% [" + "#"*progress + " "*(100-progress)+ "]", end="\r")

    resized = cv2.resize(frame, dsize=frameSize, interpolation=cv2.INTER_AREA)
    writer.write(resized)

    #  if not length % samples_interval == 0:
    #      continue
    
    #resized = cv2.resize(frame, dsize=frameSize, interpolation=cv2.INTER_AREA)
    #writer.write(resized)
    


cap.release()
writer.release()
