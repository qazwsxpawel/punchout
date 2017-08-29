from datetime import datetime, timedelta
from pathlib import Path

from sh import jrnl

# TODO: # pomodoros
# TODO: # geeknote
# TODO: # pocket
# TODO: # numbers
# TODO: # items added
# TODO: # items done


def _screen_time(start_date):
    counters_dir = Path(Path.home() / 'Dropbox' / 'time_tracking')
    # generate dates in the timerange from `start_date`
    dates = [datetime.now()]
    for i in range((datetime.now() - start_date).days):
        dates.append(start_date + timedelta(days=i))

    # count mins in the timerange
    counter = 0
    for d in dates:
        day_file = 'day-{:%Y-%m-%d}.txt'.format(d)
        current_counter = Path(counters_dir / day_file)
        if not current_counter.exists():
            continue
        with open(current_counter) as c:
            counter += int(c.read().strip())

    hours = counter // 60
    mins = counter % 60
    screen_time = f"Spent {hours}hours {mins}mins staring at the screen"
    return screen_time


def _todo(start_date):
    todo_path = Path(Path.home() / 'Dropbox/todo')

    def was_done_today(line):
        when_added = datetime.strptime(line.split()[1], '%Y-%m-%d')
        return start_date - when_added < timedelta(hours=24)

    with open(todo_path / 'done.txt') as f:
        lines = f.readlines()
        done_today = ["".join(l.strip()) for l in lines if was_done_today(l)]
    return "\n".join(done_today)


def _writing(start_date):

    def modified_fromdate(f):
        mtime = f.lstat().st_mtime
        mod_date = datetime.fromtimestamp(mtime)
        return start_date - mod_date < timedelta(hours=24)

    def ignored(f):
        ignore_rules = [f.name.startswith('.'), ]
        return any(ignore_rules)

    writing = Path(Path.home() / 'Dropbox/writing')
    modified_files = [f for f in writing.iterdir() if modified_fromdate(f) and not ignored(f)]
    return "\n".join(map(lambda x: getattr(x, 'name'), modified_files))


def _jrnl(start_date):
    entries = jrnl('-from', start_date, '--short')
    return entries.strip()


def display_report(display_func=None):
    if display_func is None:
        Exception("Need to pass display function like `print` or `click.echo`")


REPORTERS = (
    (_todo, '##### TODO #####'),
    (_writing, '##### WRITING #####'),
    (_jrnl, '##### JRNL #####'),
    (_screen_time, '##### TIME #####'),
)
