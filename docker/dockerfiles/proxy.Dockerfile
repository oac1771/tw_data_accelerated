FROM openjdk:11

COPY proxy_entrypoint.sh entrypoint.sh
COPY airflow_entrypoint.sh airflow_entrypoint.sh
COPY pyproject.toml pyproject.toml

RUN apt-get update && apt-get install python3-pip -y
RUN pip install poetry
RUN poetry install

ENTRYPOINT ["sh"]