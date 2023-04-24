FROM ubuntu

RUN apt-get -y update && apt-get -y install python3 pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD ["python3", "back/app.py"]