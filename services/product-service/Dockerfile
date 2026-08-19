FROM python:3.12.3-bookworm

RUN pip install -U pip setuptools wheel

WORKDIR /project

# Utilisateur non privilegie (le conteneur ne doit pas tourner en root)
RUN groupadd --system appgroup \
 && useradd --system --gid appgroup --home-dir /project appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R root:appgroup /project && chmod -R g=rX,o= /project

USER appuser

CMD ["gunicorn", "-b", "0.0.0.0:8081", "-w", "2", "main:app"]
