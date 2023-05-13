FROM alpine:latest
COPY vote.py /scripts/
CMD [ "python", "/scripts/button.py" ]
