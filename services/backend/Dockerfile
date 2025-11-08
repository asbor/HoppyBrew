FROM python:3.14-slim

# Accept UID and GID as build arguments (defaults to 1000 if not provided)
ARG USER_UID=1000
ARG USER_GID=1000

# Install PostgreSQL client and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user with the specified UID/GID
RUN groupadd -g ${USER_GID} app || true && \
    useradd -m -s /bin/bash -u ${USER_UID} -g ${USER_GID} app

USER app

WORKDIR /home/app

COPY requirements.txt .
RUN pip3 install --user -r requirements.txt --no-cache-dir

# Ensure ~/.local/bin is in the PATH
ENV PATH="/home/app/.local/bin:${PATH}"

COPY . .

EXPOSE 8000
CMD ["/home/app/.local/bin/uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
