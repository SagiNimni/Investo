FROM python:3.10.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/
COPY InvestoAnalayzers-1.0-py3-none-any.whl /code/

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /code/
