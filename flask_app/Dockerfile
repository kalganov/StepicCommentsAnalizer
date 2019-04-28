FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

RUN apt-get install -y python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV PYTHONIOENCODING utf8

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]