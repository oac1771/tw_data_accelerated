location of spark scripts:  /opt/homebrew/Cellar/apache-spark/3.3.1/libexec/sbin

start docker container: docker run -it --entrypoint "sh" spark:latest

repo that has data and requirements:
https://github.com/data-derp/exercise-co2-vs-temperature-databricks

to run emissions (data ingestion part): python scripts/emissions.py