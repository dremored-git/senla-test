FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY pyproject.toml ./
COPY zags ./zags
COPY tests ./tests
RUN pip install --no-cache-dir ".[dev,defense]"
CMD ["pytest", "tests/unit", "tests/final_support", "-v"]
