FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root
COPY . .

#COPY /requirements.txt /
#
#RUN pip install -r /requirements.txt --no-cache-dir
#
#COPY . .
#CMD ["poetry", "run", "sh", "-c", "python manage.py migrate && python manage.py csu && python manage.py runserver 0.0.0.0:8000"]