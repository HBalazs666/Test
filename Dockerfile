FROM python:3.9-bullseye

LABEL image="proba"

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --deploy --system

COPY . .

EXPOSE 5000

CMD ["python3", "./main.py"]
