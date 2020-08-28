FROM python:3.8.5-buster

RUN mkdir -p /app/src

WORKDIR /app/src

COPY requirements.txt .

RUN pip3.8 install -r requirements.txt

COPY . /app/src

EXPOSE 8000

CMD ["python3.8","manage.py","runserver"]








