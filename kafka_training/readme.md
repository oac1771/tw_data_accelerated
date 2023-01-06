good resource on kafka networking: https://www.confluent.io/blog/kafka-listeners-explained/

you must edit the advertised.listeners property in kafka_2.13-3.3.1/config/kraft/server.properties to be
equal to bootstrap_server field in your python scripts