import typer

from apps.telegram_bot.app import bot_start as telegram_bot_start

app = typer.Typer()


@app.command()
def start_telegram_bot(watch: bool = typer.Option(False, help="Watch mode enabled"),):
    if watch:
        devModeTag = "DEV MODE"
    else:
        devModeTag = ""

    typer.echo(f"Telegram Bot running...{devModeTag}")

    telegram_bot_start()


if __name__ == "__main__":
    app()
