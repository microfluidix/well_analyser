FROM python:latest
WORKDIR /root
COPY . .
RUN python -V &&\
    pip install .
CMD python -V && /bin/bash