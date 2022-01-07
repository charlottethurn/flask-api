FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip3 install pipenv

RUN pipenv install --system --deploy

EXPOSE 5000

CMD ["python3", "app.py"]