FROM openjdk:11

RUN wget https://archive.apache.org/dist/kafka/3.3.1/kafka_2.13-3.3.1.tgz
RUN tar xvf kafka_2.13-3.3.1.tgz && mv kafka_2.13-3.3.1 kafka

COPY kafka_broker_entrypoint.sh kafka/entrypoint.sh
COPY kafka_kraft_server.properties kafka/config/kraft/server.properties

WORKDIR kafka

ENTRYPOINT ["sh"]