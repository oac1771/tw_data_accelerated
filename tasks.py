import tempfile
import shutil
from invoke import task

PATH_TO_SPARK_DEPENDENCIES = "/opt/homebrew/Cellar/apache-spark/3.3.1/libexec/"

@task
def start_local(ctx):
    ctx.run(f'docker run -d -p 8080:8080 spark:latest entrypoint.sh')


@task
def build_docker(ctx):

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(src=PATH_TO_SPARK_DEPENDENCIES, dst=f"{temp_dir}/libexec")
        shutil.copytree(src="docker/", dst=f"{temp_dir}/docker")
        shutil.copy(src="docker/entrypoint.sh", dst=temp_dir)

        with ctx.cd(temp_dir):
            ctx.run("docker build -f docker/spark.Dockerfile . -t spark:latest")

