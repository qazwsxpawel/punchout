from datetime import datetime, timedelta
from sh import jrnl
from pathlib import Path


def _todo():
    todo_path = Path(Path.home() / 'Dropbox/todo')

    def was_done_today(line):
        when_added = datetime.strptime(line.split()[1], '%Y-%m-%d')
        return datetime.now() - when_added < timedelta(hours=24)

    with open(todo_path / 'done.txt') as f:
        lines = f.readlines()
        done_today = ["".join(l) for l in lines if was_done_today(l)]
    return "\n".join(done_today)


def _writing():

    def modified_today(f):
        mtime = f.lstat().st_mtime
        mod_date = datetime.fromtimestamp(mtime)
        return datetime.now() - mod_date < timedelta(hours=24)

    def ignored(f):
        ignore_rules = [f.name.startswith('.'), ]
        return any(ignore_rules)

    writing = Path(Path.home() / 'Dropbox/writing')
    modified_files = [f for f in writing.iterdir() if modified_today(f) and not ignored(f)]
    return "\n".join(map(lambda x: getattr(x, 'name'), modified_files))


def _jrnl():
    return jrnl('-on', 'today', '--short')


def display_report(display_func=None):
    if display_func is None:
        Exception("Need to pass display function like `print` or `click.echo`")

    def display(report_gen, header):
        display_func(header)
        display_func(report_gen())

    reporters = (
        (_todo, '##### TODO #####'),
        (_writing, '##### WRITING #####'),
        (_jrnl, '##### JRNL #####'),
    )
    for report_gen, header in reporters:
        display(report_gen, header) if report_gen() else ""

    # geeknote
    # pocket
    # numbers
    # items added
    # items done
