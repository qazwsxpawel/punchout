import sys
import random
from subprocess import run, PIPE
from pathlib import Path
from datetime import date, datetime, timedelta
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
    sdate = _parse_date(sdate)
    if ctx.invoked_subcommand is None:
        # run default command
        get_day_summary(sdate)
    else:
        ctx.ensure_object(dict)
        ctx.obj['sdate'] = sdate


def _gen_report_display(sdate, reporters):
    for report_gen, header in reporters:
        display_report(partial(report_gen, sdate), header) if report_gen(sdate) else ""


def get_day_summary(sdate):
    click.echo("punchout!")
    click.echo("nighty night")
    dark_mode()
    change_wallpaper()
    _gen_report_display(sdate, report.REPORTERS)
    click.echo(wiki.get_tfa(*get_page()))
    click.echo("Sleep tight 😴 ")


@cli.command()
@click.pass_context
def stats(ctx):
    click.echo("### STATS ###")
    # week start by default
    start_date = ctx.obj['sdate'] - timedelta(days=ctx.obj['sdate'].weekday())
    _gen_report_display(start_date, report.STAT_GENS)
