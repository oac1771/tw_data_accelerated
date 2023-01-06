FROM openjdk:11

COPY kafka_2.13-3.3.1/ kafka_2.13-3.3.1/
COPY entrypoint.sh kafka_2.13-3.3.1/entrypoint.sh

WORKDIR kafka_2.13-3.3.1

ENTRYPOINT ["sh"]