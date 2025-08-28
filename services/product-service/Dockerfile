FROM python:3.12.3-bookworm
RUN pip install -U pip setuptools wheel
WORKDIR /project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8081
CMD ["gunicorn", "-b", "0.0.0.0:8081", "main:app"]
