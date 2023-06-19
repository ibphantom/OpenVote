# Operating System
FROM ubuntu:latest

# Install Python, pip, autoconf, and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip nano autoconf ufw openssh-server && \
    ln -s /usr/bin/clear /usr/bin/cls

#Enable ssh
#RUN ufw allow ssh
#RUN ufw allow 22
#RUN ufw enable

# Upgrade pip
RUN python3 -m pip install --upgrade pip 

# Install Python packages
RUN python3 -m pip install pycrypto
RUN python3 -m pip install pycryptodome
RUN python3 -m pip install paramiko
RUN pip3 install scapy

# Designer Information
LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.1.1" \
      org.label-schema.build-date="2023-05-22" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"
      
WORKDIR /OpenVote
COPY /scripts/start.py /OpenVote/start.py
COPY /scripts/vote.py /OpenVote/vote.py
COPY /scripts/server.py /OpenVote/server.py
COPY /scripts/FINAL.csv /OpenVote/FINAL.csv
COPY /scripts/client_info.txt /OpenVote/client_info.txt
COPY /scripts/home.py /OpenVote/home.py

RUN chmod +x /OpenVote/start.py
RUN chmod +x /OpenVote/vote.py
RUN chmod +x /OpenVote/server.py
RUN chmod +x /OpenVote/FINAL.csv
RUN chmod +x /OpenVote/home.py

ENV PORT 8000
ENV NEXT_TELEMETRY_DISABLED 1
EXPOSE 8000
ENV HOSTNAME OpenVoteNode
CMD HOSTNAME

WORKDIR /OpenVote
CMD ["python3", "/OpenVote/start.py"]
