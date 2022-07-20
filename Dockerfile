FROM python:3.10-bullseye

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --deploy --system

COPY . .

EXPOSE 5000

CMD ["python3", "./main.py"]
