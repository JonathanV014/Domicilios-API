FROM python:3.11-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "pipenv run python manage.py migrate && pipenv run python manage.py collectstatic --noinput && pipenv run python manage.py runserver 0.0.0.0:8000"]