FROM openjdk:11

COPY proxy-entrypoint.sh entrypoint.sh

RUN apt-get update && apt-get install python3-pip -y
RUN pip install poetry

ENTRYPOINT ["sh"]