# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.10-slim

# ── System dependencies ────────────────────────────────────────────────────────
# libgl1 + libglib2.0 are required by OpenCV (even the headless build)
# libgomp1 is required by TensorFlow / numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ── HuggingFace Spaces: run as non-root user (uid 1000) ───────────────────────
RUN useradd -m -u 1000 appuser

# ── Working directory ──────────────────────────────────────────────────────────
WORKDIR /app

# ── Install Python dependencies ────────────────────────────────────────────────
# Copy requirements first so Docker can cache this layer independently
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project files ─────────────────────────────────────────────────────────
COPY . .

# ── Ownership ─────────────────────────────────────────────────────────────────
RUN chown -R appuser:appuser /app
USER appuser

# ── Environment ───────────────────────────────────────────────────────────────
# PORT 7860 is the default for HuggingFace Spaces
ENV PORT=7860
# Keeps Python from buffering stdout/stderr (important for HF logs)
ENV PYTHONUNBUFFERED=1
# Suppress TensorFlow info/warning logs — only show errors
ENV TF_CPP_MIN_LOG_LEVEL=2

# ── Run with Gunicorn (production WSGI server) ─────────────────────────────────
# 1 worker keeps memory usage low on free-tier HF Spaces
# timeout 120 gives TensorFlow time to load the FaceNet model on cold start
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "120", "app:app"]
