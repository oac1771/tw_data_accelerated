import tempfile
from invoke import task

PATH_TO_SPARK_DEPENDENCIES = "/opt/homebrew/Cellar/apache-spark/3.3.1/libexec/"

@task
def start_local(_):
    pass


@task
def build_docker(ctx):
    # copy dockerfile into temp_dir
    # copy spark dependencies into temp_dir
    # build docker with those spark dependencies
    # use ctx.cd thing into temp_dir

    with tempfile.TemporaryDirectory() as temp_dir:
        print('created temporary directory', temp_dir)

    # ctx.run("docker build -f docker/spark.Dockerfile . -t spark:latest")

