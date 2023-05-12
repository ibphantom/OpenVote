FROM alpine:latest
COPY button.py vote.py /app/
CMD [ "python", "/app/button.py" ]
