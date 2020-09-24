FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

RUN apt update

RUN apt install libgl1-mesa-glx -y

COPY . /usr/src/app

EXPOSE 8008


CMD python app.py
