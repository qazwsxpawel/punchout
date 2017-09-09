from datetime import datetime, timedelta
from pathlib import Path

from sh import jrnl


def _dates_from(start_date):
    """Generate dates in the timerange from `start_date`"""
    dates = [datetime.now()]
    for i in range((datetime.now() - start_date).days):
        dates.append(start_date + timedelta(days=i))
    return dates


def _screen_time(start_date):
    counters_dir = Path(Path.home() / 'Dropbox' / 'time_tracking')
    dates = _dates_from(start_date)

    # count mins in the timerange
    day_times = []
    days_count = 0
    for d in dates:
        day_file = 'day-{:%Y-%m-%d}.txt'.format(d)
        current_counter = Path(counters_dir / day_file)
        if not current_counter.exists():
            continue
        with open(current_counter) as c:
            days_count += 1
            day_times.append(int(c.read().strip()))

    counter = sum(day_times)
    hours = counter // 60
    mins = counter % 60
    days_count
    return {'hours': hours, 'mins': mins, 'days_count': days_count, 'day_times': day_times}


def _screen_time_stats(start_date):
    st = _screen_time(start_date)
    avg = float(st['hours']) / st['days_count']
    top = max(st['day_times']) / 60.0
    bottom = min(st['day_times']) / 60.0
    total = sum(st['day_times']) / 60.0
    return {'total': total, 'avg': avg, 'top': top, 'bottom': bottom, 'start_date': start_date}


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
    (lambda sdate: "Spent {hours}hours {mins}mins staring at the screen".format(**_screen_time(sdate)), '##### TIME #####'),
)


STAT_GENS = (
    (lambda sdate: "From: {start_date:%Y-%m-%d}--Total: {total:.3}, Avg.: {avg:.3}, Top: {top:.3}, Bottom: {bottom:.3}".format(**_screen_time_stats(sdate)), '##### TIME #####'),
)
