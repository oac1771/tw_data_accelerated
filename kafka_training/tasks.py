import tempfile
import shutil

from invoke import task
from jinja2 import Environment, FileSystemLoader

@task
def start_local(ctx):
    rendered_compose = render_compose()

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

        # shutil.copy(src="scripts/pyproject.toml", dst=f"{temp_dir}/docker/pyproject.toml")

        with ctx.cd(f"{temp_dir}/docker"):
            ctx.run("docker build -f kafka.Dockerfile . -t kafka:latest --no-cache")
            # ctx.run("docker build -f proxy.Dockerfile . -t proxy:latest")


def render_compose():
    environment = Environment(loader=FileSystemLoader("docker/"))
    template = environment.get_template("docker-compose.yml.jinja")

    f = template.render()
    return f
