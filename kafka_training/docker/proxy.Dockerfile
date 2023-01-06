FROM openjdk:11

COPY scripts/ scripts/
COPY proxy-entrypoint.sh entrypoint.sh

WORKDIR scripts/

RUN apt-get update && apt-get install python3-pip -y
RUN pip install poetry
RUN poetry install

ENTRYPOINT ["sh"]