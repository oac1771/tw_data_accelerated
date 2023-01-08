Kafka stuff:

good resource on kafka networking: https://www.confluent.io/blog/kafka-listeners-explained/

you must edit the advertised.listeners property in kafka_2.13-3.3.1/config/kraft/server.properties to be
equal to ip of host machine (PLAINTEXT://host.docker.internal:9092) variable in your tasks.py file



Spark stuff:

repo that has data and requirements:
https://github.com/data-derp/exercise-co2-vs-temperature-databricks

where to get students.json data: https://github.com/data-derp/small-exercises/blob/master/wrangling-in-spark/wrangling-in-spark/wrangling-in-spark/init_data.py

where to get csv files: https://github.com/data-derp/exercise-co2-vs-temperature-databricks/tree/master/data-ingestion/input-data



General stuff:

docker exec -it << container name >> /bin/bash -c "poetry shell && sh"
start docker container from image: docker run -it --entrypoint "sh" spark:latest