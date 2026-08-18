FROM python:3.12.3-bookworm
#FROM python:3.12-alpine


RUN pip install -U \
    pip \
    setuptools \
    wheel

WORKDIR /project

RUN groupadd --system appgroup \
&& useradd --system --gid appgroup --home-dir /project appuser

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chown -R root:appgroup /project && chmod -R g=rX,o= /project

ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}

USER appuser

CMD [ "python", "main.py" ]
