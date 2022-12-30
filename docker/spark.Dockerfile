FROM openjdk:11

COPY libexec/ libexec/

CMD ["java", "Main"]
