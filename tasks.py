import tempfile
import shutil
from invoke import task

PATH_TO_SPARK_DEPENDENCIES = "/opt/homebrew/Cellar/apache-spark/3.3.1/libexec/"

@task
def start_local(ctx):
    with ctx.cd("docker"):
        ctx.run("docker compose up -d")

@task
def stop_local(ctx):
    with ctx.cd("docker"):
        ctx.run("docker compose down")


@task
def docker_build(ctx):

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(src=PATH_TO_SPARK_DEPENDENCIES, dst=f"{temp_dir}/libexec")
        shutil.copytree(src="docker/", dst=f"{temp_dir}/docker")
        shutil.copy(src="docker/entrypoint.sh", dst=temp_dir)
        shutil.copy(src="docker/proxy-entrypoint.sh", dst=temp_dir)

        with ctx.cd(temp_dir):
            ctx.run("docker build -f docker/spark.Dockerfile . -t spark:latest")
            ctx.run("docker build -f docker/proxy.Dockerfile . -t proxy:latest")

