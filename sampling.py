
import cv2
import boto3

import os
import sys
sys.stdout.flush()


class VideoSampler():
    def __init__(self, config):
        self.src_bucket = config.src_bucket
        self.dst_bucket = config.dst_bucket
        

    def process(self, video_name, out_name):

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

        for i in range(1000):
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

    def download_video(self, download_path):
        self.src_bucket.download_file(download_path, self._get_name(download_path))
        print(f"{download_path} downloaded")
    
    def upload_image(self, upload_path):
        self.dst_bucket.upload_file(self._get_name(upload_path), upload_path)
        print(f"{upload_path} uploaded")


    def _get_name(self, path):
        return path.split('/')[-1]


class SamplerConfig():
    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.src_bucket = self.s3.Bucket('panoramic-videos')
        self.dst_bucket = self.s3.Bucket('extracted-panoramic-images')




if __name__ == "__main__":

    
    config = SamplerConfig()
    svc = VideoSampler(config=config)


    video_name = "NVR-CH01_S20210817-000000_E20210817-001334.mp4"
    out_name = "out_" + video_name


    svc.download_video(f"{17}/{video_name}")

    svc.process(video_name=video_name, out_name=out_name)

    svc.upload_image(f"test/{out_name}")


    os.remove(video_name)
    os.remove(out_name)

