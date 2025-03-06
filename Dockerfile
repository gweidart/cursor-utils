FROM python:3.10-slim

WORKDIR /app

# Install UV
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements/requirements.txt .
RUN /root/.cargo/bin/uv pip install --system -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the application
RUN /root/.cargo/bin/uv pip install --system -e .

# Set the entrypoint
ENTRYPOINT ["cursor-utils"]
CMD ["--help"] 