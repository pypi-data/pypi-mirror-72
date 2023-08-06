#
# Copyright (c) 2020, onceml.com
#

from onceml.sync import sync as run_sync

import typer
import os

app = typer.Typer()


@app.command()
def mlflow(project: str = ""):
    default_project = os.environ.get("ONCEML_PROJECT", None)
    if default_project:
        typer.echo(f"project: {default_project}")
    elif "" == project:
        message = typer.style(
            "ONCEML_PROJECT", fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True,
        )
        typer.echo(
            f"\nMissing project qualified name. Use {message} environment variable or pass it as an argument\n"
        )
    else:
        typer.echo(f"project: {project}")
        path = os.getcwd()  # "./"
        run_sync(path=path, project=project)


# @app.command()
# def goodbye(name: str, formal: bool = False):
#     if formal:
#         typer.echo(f"Goodbye Ms. {name}. Have a good day.")
#     else:
#         typer.echo(f"Bye {name}!")


def main():
    app()


if __name__ == "__main__":
    app()
