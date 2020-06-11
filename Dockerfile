FROM python:latest
WORKDIR /root
COPY . .
RUN python -V &&\
    pip install -r requirements.txt
CMD python -V && /bin/bash