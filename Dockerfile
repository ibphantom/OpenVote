# Operating System
FROM ubuntu:20.04
# Updates | Install Python | Assure clear command is linked to cls command
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/clear /usr/bin/cls
   
RUN pip install pycrypto
RUN pip install pycryptodome
#Designer Information
LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.0.1" \
      org.label-schema.build-date="2023-05-12" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"
      
WORKDIR /VOTE
COPY scripts/vote.py /VOTE/vote.py
COPY scripts/Generate.py /VOTE/generate.py

ENV PORT 8000
ENV NEXT_TELEMETRY_DISABLED 1
EXPOSE 8000



WORKDIR /VOTE
CMD ["python3", "generate.py"]
