# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_main.ipynb.

# %% auto 0
__all__ = ['app', 'version', 'config', 'sync_feeds', 'config_exists', 'init']

# %% ../nbs/00_main.ipynb 3
import os
import typer
from dotenv import load_dotenv
from typing import Optional
from typing_extensions import Annotated
from . import __version__
from .feeds import sync_feeds as sf, connect_feeds_db, create_feeds_db, create_articles_db, sync_feeds_db_from_cache, get_articles_lang_per_feeds, update_feeds_with_languages
from rich import print

# %% ../nbs/00_main.ipynb 5
app = typer.Typer()

# %% ../nbs/00_main.ipynb 7
@app.command()
def version():
    """Get the current installed version of ReadNext"""
    print(f"Version: {__version__}")

# %% ../nbs/00_main.ipynb 10
@app.command()
def config():
    """Get the current configuration of the Small Web Feeds Processor tool"""
    print(f"FEEDS_PATH: {os.environ.get('FEEDS_PATH')}")
    print(f"DB_PATH: {os.environ.get('DB_PATH')}")

# %% ../nbs/00_main.ipynb 13
@app.command()
def sync_feeds(ddmmyyyy: Annotated[Optional[str], typer.Argument()] = None):
    """Sync all the feeds from the Small Web index. If `ddmmyyyy` is provided, sync 
    the feeds from that day. Default is today."""
    if ddmmyyyy is None:
        print("Downloading today's feeds...")
        sf()
    print("Synchronizing the feeds db with the local cache...")
    if ddmmyyyy is None:
        sync_feeds_db_from_cache()
    else:
        sync_feeds_db_from_cache(ddmmyyyy)
    print("Updating the feeds' language...")
    update_feeds_with_languages(get_articles_lang_per_feeds())

# %% ../nbs/00_main.ipynb 15
def config_exists(env_var: str):
    """Check if `env_var` environment variable exists"""
    v = env_var.upper()
    if not os.environ.get(v) or os.environ.get(v) == '':
        print("[bold red]Error:[/bold red] [italic red]Configuration option not set.[/italic red] [yellow]Please set the [bold]" + v + "[/bold] environment variable.[/yellow]\n")

# %% ../nbs/00_main.ipynb 16
def init():
    """Initialize the application"""
    # load environment variables
    load_dotenv()

    # check for the existance of all configuration options
    config_exists('FEEDS_PATH')
    config_exists('DB_PATH')
    config_exists('MODEL_PATH')

    # Create the feeds database if it doesn't exist
    if not os.path.exists(os.environ.get('DB_PATH')):
        print("[Cyan]Feeds database not existing, creating...")
        conn = connect_feeds_db()
        create_feeds_db(conn)
        create_articles_db(conn)
        conn.close()

    # run app after initialization
    app()

# %% ../nbs/00_main.ipynb 18
#| eval: false
if __name__ == "__main__":
    init()
