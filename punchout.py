from subprocess import run, PIPE
import random
from pathlib import Path

import click

from sh import dark_mode

import bye
import report


def switch_to_dark_mode():
    dark_mode()


def change_wallpaper():
    wallpaper_dir = Path(Path.home() / 'Documents/wallpapers')
    pngs = wallpaper_dir.glob('*.png')
    jpgs = wallpaper_dir.glob('*.jpg')
    wallpapers = list(pngs) + list(jpgs)
    random_wallpaper_path = random.choice(wallpapers)
    scpt = f"""tell application "Finder" to set desktop picture to "{random_wallpaper_path}" as POSIX file"""
    run(['osascript', '-e', scpt], stdin=PIPE, stdout=PIPE, stderr=PIPE)


@click.command()
def cli():
    click.echo("punchout!")
    switch_to_dark_mode()
    change_wallpaper()
    report.display_report(display_func=click.echo)
    bye.bye_message()
