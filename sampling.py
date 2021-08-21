
import cv2
import boto3

import os
import sys
sys.stdout.flush()


class VideoSampler():
    def __init__(self, s3, src_bucket_name, dst_bucket_name):
        self.src_bucket = s3.Bucket(src_bucket_name)
        self.dst_bucket = s3.Bucket(dst_bucket_name)
        

    def process(video_name, out_name):

        print("cature created")
        cap = cv2.VideoCapture(video_name)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        frameSize = (int(width/4), int(height/4))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(out_name, fourcc, fps, frameSize)

        print(f"org length: {length}")
        print(f"org fps: {fps}")
        print(f"org dimension: {width}, {height}")
        print(f"out dimension: {width/4}, {height/4}")
        print(f"out fps: {fps}")

        print("capture start")

        for i in range(100):
            ret, frame = cap.read()
            if not ret:
                cap.release()
                writer.release()
                break

            progress = int(i/length*100)
            print(f"{i}/{length} {progress}% [" + "#"*progress + " "*(100-progress)+ "]")

            resized = cv2.resize(frame, dsize=frameSize, interpolation=cv2.INTER_AREA)
            writer.write(resized)

            
        writer.release()
        cap.release()

        print("release")

    def download_video(download_path):
        self.src_bucket.download_file(download_path, self._get_name(download_path))
        print(f"{download_path} downloaded")
    
    def upload_image(upload_path):
        self.dst_bucket.upload_file(self._get_name(upload_path), upload_path)
        print(f"{upload_path} uploaded")


    def _get_name(path):
        return path.split('/')[-1]








if __name__ == "__main__":
    date = 17

    s3 = boto3.resource('s3')

    svc = VideoSampler( s3=s3,
                        src_bucket_name='panoramic-videos', 
                        dst_bucket_name='extracted-panoramic-images')


    video_name = "NVR-CH01_S20210817-000000_E20210817-001334.mp4"
    download_path = f"{date}/{video_name}"
    svc.download_video(download_path)


    svc.process(video_name=video_name, out_name=out_name)


    out_name = "out_" + video_name
    upload_path = f"test/{out_name}"
    svc.upload_image(upload_path)


    os.remove(video_name)
    os.remove(out_name)

