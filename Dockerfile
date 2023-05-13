FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y python3-pip

LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.0.1" \
      org.label-schema.build-date="2023-05-12" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"

WORKDIR /app

RUN pip3 install flask

COPY . .

COPY scripts/vote.py /app/vote.py

EXPOSE 8000

CMD ["python3", "vote.py"]
