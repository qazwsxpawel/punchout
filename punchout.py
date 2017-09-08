import sys
import random
from subprocess import run, PIPE
from pathlib import Path
from datetime import date, datetime
from functools import partial

import click
import requests
from sh import dark_mode

import wiki
import report


def wallpaper_change_scpt():
    wallpaper_dir = Path(Path.home() / 'Documents/wallpapers')
    pngs = wallpaper_dir.glob('*.png')
    jpgs = wallpaper_dir.glob('*.jpg')
    wallpapers = list(pngs) + list(jpgs)
    random_wallpaper_path = random.choice(wallpapers)
    return f"""tell application "Finder" to set desktop picture to "{random_wallpaper_path}" as POSIX file"""


def change_wallpaper():
    run(['osascript', '-e', wallpaper_change_scpt()],
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE)


def display_report(report_gen, header):
    click.echo(header)
    click.echo(report_gen())


def get_page():
    # the feature of the day
    wiki_tfa = "https://en.wikipedia.org/api/rest_v1/feed/featured/{:%Y/%m/%d}"
    wiki_page = "https://en.wikipedia.org/?curid={}"
    today = date.today()
    return (requests.get(wiki_tfa.format(today), wiki_page), wiki_page)


def _parse_date(sdate):
    delims = ['/', '.', '-']
    ymd = "%Y{delim}%m{delim}%d"
    dmy = "%d{delim}%m{delim}%Y"
    fmts = [*[ymd.format(delim=d) for d in delims], *[dmy.format(delim=d) for d in delims]]
    success = False
    for _fmt in fmts:
        try:
            sdate = datetime.strptime(sdate, _fmt)
            success = True
            break
        except ValueError as e:
            pass
    if not success:
        click.echo("Wrong date format, should be year-month-day")
        sys.exit(2)
    return sdate


@click.group(invoke_without_command=True)
@click.option('--sdate', default=datetime.strftime(datetime.now(), "%Y-%m-%d"), help='Start date for raport')
@click.pass_context
def cli(ctx, sdate):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
        sdate = _parse_date(sdate)
        click.echo("punchout!")

        dark_mode()
        click.echo("nighty night")

        change_wallpaper()

        for report_gen, header in report.REPORTERS:
            display_report(partial(report_gen, sdate), header) if report_gen(sdate) else ""

        click.echo("Sleep tight 😴 ")
        click.echo(wiki.get_tfa(*get_page()))
    else:
        ctx.ensure_object(dict)
        ctx.obj['sdate'] = sdate
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)


@cli.command()
@click.pass_context
def stats(ctx):
    click.echo(f"Here are some stats from {ctx.obj['sdate']}:\n")
