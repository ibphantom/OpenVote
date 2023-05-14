FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/clear /usr/bin/cls

WORKDIR /VOTE
LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.0.1" \
      org.label-schema.build-date="2023-05-12" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"

COPY scripts/vote.py /scripts/vote.py

ENV PORT 8000
ENV NEXT_TELEMETRY_DISABLED 1

EXPOSE 8000

CMD python3 /scripts/vote.py && tail -f /dev/null
