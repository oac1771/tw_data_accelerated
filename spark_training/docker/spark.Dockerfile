FROM openjdk:11

COPY libexec/ libexec/
COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["sh"]