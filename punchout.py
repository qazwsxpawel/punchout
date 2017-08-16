import random
from subprocess import run, PIPE
from pathlib import Path

import click
from sh import dark_mode

import bye
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


@click.command()
def cli():
    click.echo("punchout!")

    switch_to_dark_mode()
    click.echo("nighty night")

    run(['osascript', '-e', wallpaper_change_scpt()],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE)

    bye.bye_message()

    def display_report(report_gen, header):
        click.echo(header)
        click.echo(report_gen())
    for report_gen, header in report.REPORTERS:
        display_report(report_gen, header) if report_gen() else ""
