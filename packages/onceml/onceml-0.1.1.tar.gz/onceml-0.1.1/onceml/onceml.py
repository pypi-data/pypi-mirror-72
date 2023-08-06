#
# Copyright (c) 2020, onceml.com
#


from functools import wraps

import pendulum
import typer

app = typer.Typer()


def timer(function):
    """
    Simple Decorator to measure a function execution time.
    """

    @wraps(function)
    def function_wrapper():
        start = pendulum.now()
        function()
        ellapsed_time = pendulum.now() - start
        print(f"Execution Time: {ellapsed_time.microseconds} ms.")

    return function_wrapper


@app.command("hello")
def hello_world():
    """
    Our first CLI with typer!
    """
    typer.echo("Opening blog post...")
    typer.launch("http://onceml.spacy.cn")


def main():
    app()


# if __name__ == "__main__":
#     app()
