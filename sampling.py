
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

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('extracted-panoramic-images')

    
    import random
    time_range = "-(1[4-9]|2[0-2])\d\d\d\d"
    ch1_regex= f"NVR-CH01_S2021081(4|5){time_range}_E2021\d\d\d\d-\d\d\d\d\d\d\.mp4_\d\d\d\d\d\d\.jpg"
    ch2_regex= f"NVR-CH02_S2021081(4|5){time_range}_E2021\d\d\d\d-\d\d\d\d\d\d\.mp4_\d\d\d\d\d\d\.jpg"
    ch1 = re.compile(ch1_regex)
    ch2 = re.compile(ch2_regex)

    print("get all objects..")
    objs = list(bucket.objects.all())

    def choose_objects(regex, ch):
        crowd = 15000
        superb = 3000

        print("get ch1 objects")
        filtered_objects = list(filter(lambda obj: regex(os.path.basename(obj.key)), objs))
        print(f"count: {len(filtered_objects)}")

        print(f"ch{ch} shuffling...")
        random.shuffle(filtered_objects)

        choosed = filtered_objects[:(crowd+superb)]

        crowd = choosed[:crowd]
        superb = choosed[crowd:(crowd+superb)]

        upload_to = f"crowdworks/ch{ch}"
        for i, obj in enumerate(crowd):
            filename = os.path.basename(obj.key)
            print(f"{i}/{len(crowd)} upload to: {upload_to}/{filename}")
            bucket.download_file(obj.key,  filename)
            bucket.upload_file(filename, os.path.join(upload_to, filename))


        upload_to = f"superbai/ch{ch}"
        for i, obj in enumerate(superb):
            filename = os.path.basename(obj.key)
            print(f"{i}/{len(superb)} upload to: {upload_to}/{filename}")
            bucket.download_file(obj.key,  filename)
            bucket.upload_file(filename, os.path.join(upload_to, filename))


    choose_objects(ch1.match, "1")
    choose_objects(ch2.match, "2")

    #
    #  ch2_choosed = ch2_objs[:crowd+superb]
    #
    #  ch2_crowd = ch2_choosed[:crowd]
    #  ch2_superb = ch2_choosed[crowd:superb]
    #
    #  print("get ch2 objects")
    #  ch2_objs = list(filter(lambda obj: ch2.match(obj.key), objs))
    #
    #  print("ch2 shuffling...")
    #  random.shuffle(ch2_objs)
    #
    #  upload_to = "crowdworks/ch2"
    #  for i, obj in enumerate(ch2_crowd):
    #      filename = os.path.basename(obj.key)
    #      print(f"{i}/{len(ch2_crowd)} upload to: {upload_to}/{filename}")
    #      bucket.download_file(obj.key,  filename)
    #      bucket.upload_file(filename, os.path.join(upload_to, filename))
    #
    #  upload_to = "superbai/ch2"
    #  for i, obj in enumerate(ch2_superb):
    #      filename = os.path.basename(obj.key)
    #      print(f"{i}/{len(ch2_superb)} upload to: {upload_to}/{filename}")
    #      bucket.download_file(obj.key,  filename)
    #      bucket.upload_file(filename, os.path.join(upload_to, filename))
    #


    exit()

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




