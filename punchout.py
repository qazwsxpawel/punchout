import random
from subprocess import run, PIPE
from pathlib import Path
from datetime import date

import click
import requests
from sh import dark_mode

import wiki
import report


def switch_to_dark_mode():
    dark_mode()


def wallpaper_change_scpt():
    wallpaper_dir = Path(Path.home() / 'Documents/wallpapers')
    pngs = wallpaper_dir.glob('*.png')
    jpgs = wallpaper_dir.glob('*.jpg')
    wallpapers = list(pngs) + list(jpgs)
    random_wallpaper_path = random.choice(wallpapers)
    return f"""tell application "Finder" to set desktop picture to "{random_wallpaper_path}" as POSIX file"""


def display_report(report_gen, header):
    click.echo(header)
    click.echo(report_gen())


def get_page():
    # the feature of the day
    wiki_tfa = "https://en.wikipedia.org/api/rest_v1/feed/featured/{:%Y/%m/%d}"
    wiki_page = "https://en.wikipedia.org/?curid={}"
    today = date.today()
    return (requests.get(wiki_tfa.format(today), wiki_page), wiki_page)


@click.command()
def cli():
    click.echo("punchout!")

    switch_to_dark_mode()
    click.echo("nighty night")

    run(['osascript', '-e', wallpaper_change_scpt()],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE)

    for report_gen, header in report.REPORTERS:
        display_report(report_gen, header) if report_gen() else ""

    click.echo("Sleep tight 😴 ")
    click.echo(wiki.get_wiki(*get_page()))
