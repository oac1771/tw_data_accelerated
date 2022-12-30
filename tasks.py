from invoke import task

@task
def start_local(_):
    pass


@task
def build_docker(ctx):

    ctx.run("docker build -f docker/spark.Dockerfile . -t spark:latest")
    
