FROM openjdk:11

COPY proxy-entrypoint.sh entrypoint.sh
COPY pyproject.toml scripts/pyproject.toml

WORKDIR scripts/

RUN apt-get update && apt-get install python3-pip -y
RUN pip install poetry
RUN poetry install

ENTRYPOINT ["sh"]