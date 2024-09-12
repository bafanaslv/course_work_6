FROM python:3.12-slim

WORKDIR /app

# Настраиваем переменные окружения для poetry
#ENV POETRY_VERSION=1.8.3
#ENV POETRY_HOME=/opt/poetry
#ENV POETRY_VENV=/opt/poetry-venv
#ENV POETRY_CACHE_DIR=/opt/.cache
#
## Устанавливаем poetry
#RUN python3 -m venv $POETRY_VENV \
#    && $POETRY_VENV/bin/pip install -U pip setuptools \
#    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}
#
## Добавляем poetry в переменную окружения PATH
#ENV PATH="${PATH}:${POETRY_VENV}/bin"
#
## Установка зависимостей
#COPY poetry.lock pyproject.toml ./
#RUN poetry install

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .
CMD ["sh", "-c", "python manage.py migrate && python manage.py csu && python manage.py runserver 0.0.0.0:8000"]