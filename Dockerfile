FROM nvcr.io/nvidia/pytorch:24.12-py3

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/app/venv/bin:/root/.local/bin:$PATH"

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN mkdir -p /app

WORKDIR /app
COPY requirements.txt .
RUN uv venv /app/venv
RUN uv pip install -r requirements.txt
COPY main.py .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]