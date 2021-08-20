
FROM jrottenberg/ffmpeg:3-ubuntu AS l1

FROM python:3.9.6-buster AS l2
WORKDIR /tmp/workdir
COPY --from=l1 /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=l1 /usr/local/lib/* /usr/local/lib/

ENTRYPOINT bash
