FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml ./

RUN python -m pip install --upgrade pip && \
    python -c "import pathlib, subprocess, sys, tomllib; deps = tomllib.loads(pathlib.Path('pyproject.toml').read_text(encoding='utf-8'))['project']['dependencies']; subprocess.check_call([sys.executable, '-m', 'pip', 'install', *deps])"

COPY src ./src

WORKDIR /app/src

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]