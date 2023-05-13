FROM alpine:3.15

LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.0.1" \
      org.label-schema.build-date="2023-05-12" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"

RUN apk add --no-cache python3 py3-pip

COPY scripts/vote.py /scripts/vote.py

CMD python3 /scripts/vote.py
