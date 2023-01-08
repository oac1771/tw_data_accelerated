FROM openjdk:11

COPY libexec/ libexec/
COPY spark_entrypoint.sh entrypoint.sh

ENTRYPOINT ["sh"]