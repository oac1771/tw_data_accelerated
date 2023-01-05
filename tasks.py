import tempfile
import shutil

from invoke import task
from jinja2 import Environment, FileSystemLoader

PATH_TO_SPARK_DEPENDENCIES = "/opt/homebrew/Cellar/apache-spark/3.3.1/libexec/"

@task
def start_local(ctx, number_of_workers=2):
    rendered_compose = render_compose(number_of_workers=number_of_workers)

    with open("docker/docker-compose.yml", mode="w+", encoding="utf-8") as f:
        f.write(rendered_compose)
    ctx.run("docker compose -f docker/docker-compose.yml up -d")

@task
def stop_local(ctx):
    with ctx.cd("docker"):
        ctx.run("docker compose down")

@task
def docker_build(ctx):

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(src="docker/", dst=f"{temp_dir}/docker")

        shutil.copytree(src=PATH_TO_SPARK_DEPENDENCIES, dst=f"{temp_dir}/docker/libexec/")
        shutil.copy(src="scripts/pyproject.toml", dst=f"{temp_dir}/docker/pyproject.toml")

        with ctx.cd(f"{temp_dir}/docker"):
            ctx.run("docker build -f spark.Dockerfile . -t spark:latest")
            ctx.run("docker build -f proxy.Dockerfile . -t proxy:latest --no-cache")


def render_compose(number_of_workers):
    environment = Environment(loader=FileSystemLoader("docker/"))
    template = environment.get_template("docker-compose.yml.jinja")

    f = template.render(number_of_workers=number_of_workers)
    return f