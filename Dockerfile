FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./vochabular /code/
ADD ./scripts /code/scripts

CMD python3 manage.py runserver 0.0.0.0:8000
