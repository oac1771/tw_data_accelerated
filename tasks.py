import tempfile
import shutil
from invoke import task

PATH_TO_SPARK_DEPENDENCIES = "/opt/homebrew/Cellar/apache-spark/3.3.1/libexec/"

@task
def start_local(ctx):
    ctx.run("docker network create --driver bridge spark-net-bridge", hide=True)
    stdout = ctx.run(f"docker run --name master -d -p 8080:8080 -p 7077:7077 --network spark-net-bridge spark:latest entrypoint.sh start-master.sh", hide=True).stdout
    container_id = stdout[0:12]

    ctx.run(f"docker run --name worker -d -p 8081:8081 --network spark-net-bridge spark:latest entrypoint.sh start-worker.sh spark://{container_id}:7077", hide=True)


@task
def docker_build(ctx):

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(src=PATH_TO_SPARK_DEPENDENCIES, dst=f"{temp_dir}/libexec")
        shutil.copytree(src="docker/", dst=f"{temp_dir}/docker")
        shutil.copy(src="docker/entrypoint.sh", dst=temp_dir)

        with ctx.cd(temp_dir):
            ctx.run("docker build -f docker/spark.Dockerfile . -t spark:latest")

