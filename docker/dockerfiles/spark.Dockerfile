FROM openjdk:11

COPY spark_entrypoint.sh entrypoint.sh

RUN wget https://downloads.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz
RUN tar xvf spark-* && mv spark-3.3.1-bin-hadoop3 spark

ENTRYPOINT ["sh"]