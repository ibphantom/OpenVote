FROM alpine:latest

# Update apk packages and install Python3 and pip
RUN apk update && \
    apk add --no-cache python3 py3-pip && \
    pip install --upgrade pip

# Create and set the working directory
WORKDIR /app

# Copy the vote.py script to the container
COPY scripts/vote.py .

# Set the entry point for the container
ENTRYPOINT ["python3", "vote.py"]
