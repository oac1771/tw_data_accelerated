good resource on kafka networking: https://www.confluent.io/blog/kafka-listeners-explained/

you must edit the advertised.listeners property in kafka_2.13-3.3.1/config/kraft/server.properties to be
equal to BOOTSTRAP_SERVER variable in your tasks.py file

org.apache.kafka.common.network.InvalidReceiveException: Invalid receive (size = 1195725856 larger than 104857600)