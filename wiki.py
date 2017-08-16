import click


def _style_wiki(title, url):
    styled_text = click.style(title, fg="cyan")
    styled_url = click.style(url, bg="yellow", fg="black")
    return ": ".join([styled_text, styled_url])


def get_wiki(r, wiki_page):
    page_id = r.json()["tfa"]["pageid"]
    title = r.json()["tfa"]["normalizedtitle"]
    url = wiki_page.format(page_id)
    wiki_tfa = _style_wiki(title, url)
    return wiki_tfa
