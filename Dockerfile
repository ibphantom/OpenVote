FROM python:3.9-alpine

LABEL maintainer="ibPhantom <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="0.0.1" \
      org.label-schema.build-date="2023-05-12" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"

RUN apk update && \
    apk add --no-cache gcc musl-dev

WORKDIR /app

COPY /scripts/vote.py

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "vote.py", "runserver", "0.0.0.0:8000"]
