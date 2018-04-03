FROM ubuntu:16.04

RUN mkdir -p /site
WORKDIR /site

RUN apt-get update && apt install -y python python-pip python-dev nodejs npm curl
RUN pip install --upgrade pip
RUN pip install awscli

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

COPY gulpfile.js /site
COPY package.json /site
COPY src /site/src
RUN npm install
