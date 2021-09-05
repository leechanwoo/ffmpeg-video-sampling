
#FROM opencvcourses/opencv:440
FROM spinaweb/onnxruntime:cuda-py3-opencv


ENV AWS_ACCESS_KEY_ID=AKIATDMOZVG6PQJDVGG2
ENV AWS_SECRET_ACCESS_KEY=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
ENV AWS_DEFAULT_REGION=ap-northeast-2

RUN pip3 install boto3
