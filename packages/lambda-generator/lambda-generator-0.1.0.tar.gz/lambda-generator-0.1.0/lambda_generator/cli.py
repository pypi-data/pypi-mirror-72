import typer
import os
from .functions import create_lambda

app = typer.Typer()
current_path = os.getcwd()
module_path = os.path.dirname(os.path.realpath(__file__))
templates_path = f"{module_path}/templates/"


def main():
    app()


@app.command()
def test():
    typer.echo("Working")


@app.command()
def create(
    # template_name: str,
    project_name: str,
    project_path: str = typer.Option(
        current_path, help="Path where project should be create"
    ),
):
    template_name = "python_serverless_docker_jenkins"
    template_path = f"{templates_path}{template_name}"
    path_to_create_project = f"{project_path}/{project_name}"

    create_lambda(template_path, path_to_create_project)

    typer.echo(f"Lambda created on {path_to_create_project}")
