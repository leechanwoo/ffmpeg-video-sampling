
FROM python:3.9.6-buster 

RUN pip3 install opencv-python

ENTRYPOINT bash
