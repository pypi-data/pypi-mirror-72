
import click
from path_util import path_util
from path_util.path import Path

from create_cli import cd_hack


@click.command()
@click.argument("arg")
@click.option("--go", is_flag=True)
def cli(arg, go):

    path_string = arg

    path = Path(path_string)
    if path.exists:
        print(f"[i] Path exists: '{path_string}'")

    else:
        path_util.create_path(path_string)
        print(f"[v] Created: '{path_string}'")

    if go:
        if path.is_file_like:
            cd_hack.change_parent_process_directory(path.parent.path)
        else:
            cd_hack.change_parent_process_directory(path.path)

    return True


if __name__ == "__main__":
    cli()
