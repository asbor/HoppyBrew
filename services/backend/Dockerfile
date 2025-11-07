FROM python:3.14-slim

# Install PostgreSQL client and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash app

USER app

WORKDIR /home/app

COPY requirements.txt .
RUN pip3 install --user -r requirements.txt --no-cache-dir

# Ensure ~/.local/bin is in the PATH
ENV PATH="/home/app/.local/bin:${PATH}"

COPY . .

EXPOSE 8000
CMD ["/home/app/.local/bin/uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]
