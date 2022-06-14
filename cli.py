import typer

from app import bot_start

app = typer.Typer()


@app.command()
def start(watch: bool = typer.Option(False, help="Watch mode enabled"),):
    if watch:
        devModeTag = "DEV MODE"
    else:
        devModeTag = ""

    typer.echo(f"Bot running...{devModeTag}")

    bot_start()


if __name__ == "__main__":
    app()
