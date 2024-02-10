FROM python:3.11.8

COPY ./requirements.txt /monitoring_app/requirements.txt

WORKDIR /monitoring_app

RUN pip3 install -r requirements.txt

COPY . /monitoring_app

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD [ "manage.py", "--host=0.0.0.0"]