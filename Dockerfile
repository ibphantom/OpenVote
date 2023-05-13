FROM python:3.9-alpine

LABEL maintainer="Your Name <your.email@example.com>" \
      org.label-schema.description="A containerized version of OpenVote" \
      org.label-schema.version="1.0.0" \
      org.label-schema.build-date="2022-05-12" \
      org.opencontainers.image.source="https://github.com/ibphantom/OpenVote/"

RUN apk update && \
    apk add --no-cache gcc musl-dev

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
