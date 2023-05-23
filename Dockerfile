# Operating System
FROM rockylinux/rockylinux:8
# Install Python, pip, autoconf, and other dependencies
RUN dnf -y install python3 python3-pip nano autoconf gcc && \
    ln -s /usr/bin/clear /usr/bin/cls

# Upgrade pip
RUN pip3 install --upgrade pip 

# Install Python packages
RUN pip3 install pycrypto
RUN pip3 install pycryptodome
RUN pip3 install paramiko
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
