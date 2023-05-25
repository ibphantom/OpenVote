# Operating System
FROM ubuntu:latest

# Install Python, pip, autoconf, and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip nano autoconf gcc python3-dev && \
    ln -s /usr/bin/clear /usr/bin/cls

# Upgrade pip
RUN python3 -m pip install --upgrade pip 

# Install Python packages
RUN python3 -m pip install pycrypto
RUN python3 -m pip install pycryptodome
RUN python3 -m pip install paramiko
CMD hostname
ENV HOSTNAME VoterNode

# Designer Information
LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.1.1" \
      org.label-schema.build-date="2023-05-22" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"
      
WORKDIR /VOTE
COPY scripts/start.py /VOTE/start.py
COPY scripts/vote.py /VOTE/vote.py
COPY scripts/hostname.py /VOTE/hostname.py
COPY scripts/server.py /VOTE/server.py
COPY scripts/FINAL.csv /VOTE/FINAL.csv
COPY scripts/client_info.txt /VOTE/client_info.txt

RUN chmod +x /VOTE/start.py
RUN chmod +x /VOTE/vote.py
RUN chmod +x /VOTE/hostname.py
RUN chmod +x /VOTE/server.py
RUN chmod +x /VOTE/FINAL.csv

ENV PORT 8000
ENV NEXT_TELEMETRY_DISABLED 1
EXPOSE 8000

WORKDIR /VOTE
CMD ["python3", "/VOTE/start.py"]
