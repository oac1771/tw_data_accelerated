# Setup

To spin up your Kafka and Spark clusters, you only need python and [docker](https://www.docker.com/). This repository uses [poetry](https://python-poetry.org/), a python package manager. Installation steps can be found [here](https://python-poetry.org/docs/#installing-with-the-official-installer), however I find it easiest to use brew if you are on MacOS:

```
brew install poetry
```

Once installed, you can create a virtual environment and install the necessary dependencies to create your clusters:

```
poetry shell
```

```
poetry install
```

This repository also uses a python tool called [invoke](https://www.pyinvoke.org/) which allows you to run the functions in `tasks.py` as cli commands. We will use these functions to build the necessary docker images and create your cluster using [docker compose](https://docs.docker.com/compose/):

### build images
```
inv docker-build
```

### start clusters
```
inv start-local
```

The number of spark worker nodes is also configurable and can be changed by running the following command:

```
inv start-local --number-spark-workers=<number of workers>
```

### stop clusters
To tear down your cluster, run the following command:
```
inv stop-local
```

# Interacting with your clusters

## Spark cluster

In order to connect to the `spark-master` node, you must be inside the docker compose network. To do this, simply exec into the `spark-proxy` container using the following command:

```
docker exec -it spark-proxy /bin/bash -c "poetry shell && sh"
```

This command will exec into the container, start a poetry virtual environment, and start an sh session. Once this is done, you can run any of the python scripts in the `exercises` directory. For example:

```
python exercises/wrangling_basics/dtf_reader.py
```

---
**NOTE**

The spark scripts expect the data necessary for the spark jobs to be in `scripts/spark_training/data/` directory, and this directory is [mounted to both the workers and spark proxy containers](https://spark.apache.org/docs/latest/rdd-programming-guide.html#external-datasets)

---

Because the `spark-proxy` container has a shared volume mount with the `scripts/spark_training` directory, any edits made to the files within this directory will be reflected within the `spark-proxy` container. This means you can work within your IDE and run those scripts within the `spark-proxy` container without having to tear down and spin up the whole spark cluster, making iterative changes a bit easier

## Kafka cluster

To connect to your `kafka-broker` node, you must be inside the docker compose network. To do this, exec into either the `kafka-producer` or `kafka-consumer` containers. A full end to end workflow of a kafka producer and consumer interacting with the broker would be the following:

In one terminal session, exec into the `kafka-consumer` container and run the `consume` invoke task
```
docker exec -it kafka-consumer /bin/bash -c "poetry shell && sh"
```
```
inv consume
```

In a seperate terminal session, exec into the `kafka-producer` container and run the `produce` invoke task
```
docker exec -it kafka-producer /bin/bash -c "poetry shell && sh"
```
```
inv produce
```

Once this is complete, you should see data that is being sent from the produce in your consumer terminal session.

Both the `kafka-producer` and `kafka-consumer` containers have shared volumes  with the `scripts/kafka_training` directory, so any edits made to the files within this directory will be reflected within the `kafka` containers. This means you can work within your IDE and run those scripts within the `kafka` containers without having to tear down and spin up the whole spark cluster, making iterative changes a bit easier

## Kafka to Spark cluster connection

It is possible to run spark jobs on data that is coming from a spark broker. An example of this workflow is the following:

Exec into the `spark-proxy` container and run the following command

```
inv start-structured-stream
```

In a seperate terminal window, exec into the `kafka-producer` container and run the following command
```
inv produce
```

You should see data output in the `spark-proxy` terminal session.

If you see any errors related to a checkpoint misconfiguration, one solution is to delete the `checkpoint` directory under the `spark_training` directory.

# Supplemental material:
Kafka stuff:

good resource on kafka networking: https://www.confluent.io/blog/kafka-listeners-explained/


Spark stuff:

where to get data csv files: https://github.com/data-derp/exercise-co2-vs-temperature-databricks/tree/master/data-ingestion/input-data


