FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip wheel setuptools
RUN pip3 install -r requirements.txt

COPY . .


CMD [ "python3", "-m", "src.entrypoints.server.main"]
