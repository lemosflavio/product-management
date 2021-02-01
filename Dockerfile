FROM python:3.7.8

WORKDIR /app


COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "api/run.py"]