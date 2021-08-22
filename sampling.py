
import cv2
import boto3

import os
import re
import sys
sys.stdout.flush()


class VideoSampler():
    def __init__(self, config):
        self.src_bucket = config.src_bucket
        self.dst_bucket = config.dst_bucket
        

    def process(self, video_key, video_progress):
        vi, vcomp = video_progress
        video_path, video_name = tuple(video_key.split('/'))

        print(f"cature created {video_name}")
        cap = cv2.VideoCapture(video_name)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print(f"org length: {length}")
        print(f"org fps: {fps}")
        print(f"org dimension: {width}, {height}")
        print("capture start")

        for i in range(999999999):
            for j in range(29):
                ret, dummy = cap.read()
                del dummy
                if not ret:
                    break

            ret, frame = cap.read()
            if not ret:
                cap.release()
                break

            complete = int(length/30)
            progress = int(i/complete*100)

            image_name = video_name + "_" + f'{i}'.zfill(6) + '.jpg'
            cv2.imwrite(image_name, frame)

            upload_path = os.path.join(video_path, image_name)
            self.upload_image(upload_path)
            vprogress = int(vi/vcomp*100)
            print(f"[V progress] {vi}/{vcomp} {vprogress}% [" + "#"*vprogress + " "*(100-vprogress)+ "]")
            print(f"[I progress] {i}/{complete} {progress}% [" + "#"*progress + " "*(100-progress)+ "]")
            
        cap.release()


    def download_video(self, download_path):
        self.src_bucket.download_file(download_path, self._get_name(download_path))
        print(f"{download_path} downloaded")
        return download_path
    
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
    ay_rng = "202108(0[3-6]|09|1[0-2])-[0-1][7-9]\d\d\d\d"
    jj_rng = "2021\d\d\d\d[0-1][7-9]\d\d\d\d"

    ch1 = re.compile(f"NVR-CH01_S{ay_rng}_E2021\d\d\d\d-\d\d\d\d\d\d\.(avi|mp4)")
    ch2 = re.compile(f"NVR-CH02_S{ay_rng}_E2021\d\d\d\d-\d\d\d\d\d\d\.(avi|mp4)")
    jj = re.compile(f"_{jj_rng}_2021\d\d\d\d\d\d\d\d\d\d_0(|_1)\.avi")


    day = os.environ['CATEGORY']
    holiday = re.compile(f"NVR-CH0[1-2]_S202108{day}-\d\d\d\d\d\d_E2021\d\d\d\d-\d\d\d\d\d\d\.mp4")

    config = SamplerConfig()
    objs = list(config.src_bucket.objects.all())

    def regex(fn):
        def get_name(summ):
            return fn(summ.key.split('/')[-1])
        return get_name

    holiday_objs = list(filter(regex(holiday.match), objs))
    print(f"Number of objects: {len(holiday_objs)}")

    svc = VideoSampler(config=config)

    for i, obj in enumerate(holiday_objs):
        print(f"{i} Downloading {obj.key}")
        key = svc.download_video(obj.key)
        progress = (i, len(holiday_objs))
        svc.process(video_key=key, video_progress=progress)
        os.system("rm -rf *.mp4")
        os.system("rm -rf *.jpg")




