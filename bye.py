import datetime

import click
import requests

# the feature of the day
WIKI_TFA = "https://en.wikipedia.org/api/rest_v1/feed/featured/{:%Y/%m/%d}"
WIKI_PAGE = "https://en.wikipedia.org/?curid={}"

today = datetime.date.today()


def _style_wiki(title, url):
    styled_text = click.style(title, fg="cyan")
    styled_url = click.style(url, bg="yellow", fg="black")
    return ": ".join([styled_text, styled_url])


def get_wiki():
    r = requests.get(WIKI_TFA.format(today))
    page_id = r.json()["tfa"]["pageid"]
    title = r.json()["tfa"]["normalizedtitle"]
    url = WIKI_PAGE.format(page_id)
    wiki_tfa = _style_wiki(title, url)
    return wiki_tfa


def bye_message():
    click.echo("Sleep tight 😴 ")
    click.echo(get_wiki())
