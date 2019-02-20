FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get -y update
RUN apt-get install -y mosquitto mosquitto-clients

# install dependecies for PIL
RUN apt-get install -y \
            python3-dev python3-pip python3-setuptools \
            libffi-dev libxml2-dev libxslt1-dev \
            libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev \
            liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python3-tk

RUN pip3 install -r requirements.txt
COPY . /code/
