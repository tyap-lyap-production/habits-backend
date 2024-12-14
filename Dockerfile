FROM python:3.12.7

RUN pip install poetry

COPY ./ /back

WORKDIR /back
RUN poetry install

CMD poetry run fastapi run