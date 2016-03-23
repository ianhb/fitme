FROM python:2.7
ENV PYTHONBUFFERED 1
ENV DJANGO_SETTINGS_MODULE "fitkick.test_settings"
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
ADD ./static2/ /usr/src/app/static/
