
import cv2
import boto3
import sys
sys.stdout.flush()


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
    samples_interval = length/n

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




if __name__ == "__main__":
    date = 17
    video_name = "NVR-CH01_S20210817-000000_E20210817-001334.mp4"
    out_name = "out_" + video_name

    s3 = boto3.resource('s3')

    src_bucket = s3.Bucket('panoramic-videos')
    download_path = f"{date}/{video_name}"
    print(f"download file: {video_path}")
    src_bucket.download_file(download_path, video_name)

    main(video_name=video_name, out_name=out_name)

    smpl_bucket = s3.Bucket('extracted-panoramic-images')
    smpl_bucket.upload_file(out_name, upload_path)
    upload_path = f"test/{out_name}"
    print(f"{out_name} uploaded")


    os.remove(video_name)
    os.remove(out_name)

