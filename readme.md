## Setup
#

To spin up your Kafka and Spark clusters, you only need python and docker. This repository uses [poetry](https://python-poetry.org/), a python package manager. Installation steps can be found [here](https://python-poetry.org/docs/#installing-with-the-official-installer), however I find it easiest to use brew if you are on MacOS:

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

## Interacting with your clusters
# 

### Spark cluster

In order to connect to the spark master node, you must be inside the docker compose network. To do this, simply exec into the `spark-proxy` container using the following command:

```
docker exec -it spark-proxy /bin/bash -c "poetry shell && sh"
```

This command will exec into the container, start a poetry virtual environment, and start an sh session. Once this is done, you can run any of the python scripts in the `exercises` directory. For example:

```
python exercises/wrangling_basics/emissions.py
```

Because the `spark-proxy` container has a shared volume mount with the `scripts/spark_training` directory, any edits made to the files within this directory will be reflected within the `spark-proxy` container. This means you can work within your IDE and run those scripts within the `spark-proxy` container without having to tear down and spin up the whole spark cluster, making iterative changes a bit easier


### ignore this stuff for now:
Kafka stuff:

good resource on kafka networking: https://www.confluent.io/blog/kafka-listeners-explained/




Spark stuff:



where to get csv files: https://github.com/data-derp/exercise-co2-vs-temperature-databricks/tree/master/data-ingestion/input-data



General stuff:

docker exec -it << container name >> /bin/bash -c "poetry shell && /bin/bash"
start docker container from image: docker run -it --entrypoint "/bin/bash" spark:latest