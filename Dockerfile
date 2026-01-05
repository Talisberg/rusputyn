# Rusputyn Testing Environment
# Provides Python + Rust environment for building and testing packages

FROM rust:1.75-slim

# Install Python and build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /rusputyn

# Copy project files
COPY . .

# Create virtual environment with uv (ensure uv is in PATH)
RUN /root/.cargo/bin/uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

# Install maturin and pytest using uv
RUN /root/.cargo/bin/uv pip install maturin pytest

# Install Python dependencies for benchmarks using uv
RUN /root/.cargo/bin/uv pip install \
    charset-normalizer \
    packaging \
    python-dateutil \
    colorama \
    tabulate \
    humanize \
    validators \
    markupsafe \
    tomli

# Default command
CMD ["/bin/bash"]
