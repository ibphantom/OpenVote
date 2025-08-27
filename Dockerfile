# Start from a slim Python base
FROM python:3.12-slim

# Install system dependencies (no UFW, no autoconf)
RUN apt-get update && \
    apt-get install -y nano openssh-server && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/clear /usr/bin/cls

# Upgrade pip and install Python packages
RUN pip install --upgrade pip && \
    pip install pycrypto pycryptodome paramiko scapy

# Metadata
LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.1.1" \
      org.label-schema.build-date="2023-05-22" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"

# Copy scripts
WORKDIR /OpenVote
COPY /scripts/ ./

# Make all Python scripts executable
RUN chmod +x *.py FINAL.csv

# Environment variables
ENV PORT=8000
ENV NEXT_TELEMETRY_DISABLED=1
ENV HOSTNAME=OpenVoteNode

# Expose port and set default command
EXPOSE 8000
CMD ["python3", "/OpenVote/start.py"]
