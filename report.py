from datetime import datetime, timedelta
from pathlib import Path

from sh import jrnl, git


def display_report(display_func=None):
    if display_func is None:
        Exception("Need to pass display function like `print` or `click.echo`")


def _screen_time(start_date):
    counters_dir = Path(Path.home() / 'Dropbox' / 'time_tracking')
    dates = _all_dates_from(start_date)

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

    def done_in_time_period(line):
        when_added = datetime.strptime(line.split()[1], '%Y-%m-%d')
        return start_date - when_added < timedelta(hours=24)

    with open(todo_path / 'done.txt') as f:
        lines = f.readlines()
        done_today = ["".join(l.strip()) for l in lines if done_in_time_period(l)]
    return "\n".join(done_today)


def _writing(start_date):

    def modified_fromdate(f):
        mtime = f.lstat().st_mtime
        mod_date = datetime.fromtimestamp(mtime)
        return start_date - mod_date < timedelta(hours=24)

    writing = Path(Path.home() / 'Dropbox/writing')
    modified_files = [f for f in writing.iterdir() if modified_fromdate(f) and not _ignored_files(f)]
    return "\n".join(map(lambda x: getattr(x, 'name'), modified_files))


def _jrnl(start_date):
    entries = jrnl('-from', start_date, '--short')
    return entries.strip()


def _git(start_date):
    subheader_fmt = "--- {dirname} ---"
    dirs = Path(Path.home() / 'Projects').iterdir()
    projects = []
    for d in dirs:
        if _ignored_files(d):
            continue
        dot_git = Path(d / '.git')
        if not dot_git.exists():
            continue
        git_output = git(
            f'--git-dir={Path(d.absolute()/".git")}',
            'log',
            '--pretty=format:"%C(yellow)%h%Cred%d\\ %Creset%s%Cblue\\ [%cn]"',
            '--decorate',
            '--graph',
            '--since',
            start_date)
        projects.append((subheader_fmt.format(dirname=d.name), git_output))
    return projects


def _all_dates_from(start_date):
    """Generate dates in the timerange from `start_date`"""
    dates = [datetime.now()]
    for i in range((datetime.now() - start_date).days):
        dates.append(start_date + timedelta(days=i))
    return dates


def _ignored_files(f):
    ignore_rules = [f.name.startswith('.'), ]
    return any(ignore_rules)


def _fmt_screen_time(sdate):
    return "Spent {hours}hours {mins}mins staring at the screen".format(**_screen_time(sdate))


def _fmt_git(sdate):
    git_out = []
    for d, o in _git(sdate):
        git_out.append("Project {}:\n {}".format(d, "\n".join(o)))
    return "\n".join(git_out)


REPORTERS = (
    (_todo, '##### TODO #####'),
    (_writing, '##### WRITING #####'),
    (_jrnl, '##### JRNL #####'),
    (_fmt_git, '##### GIT #####'),
    (_fmt_screen_time, '##### TIME #####'),
)


STAT_GENS = (
    (lambda sdate: "From: {start_date:%Y-%m-%d}--Total: {total:.3}, Avg.: {avg:.3}, Top: {top:.3}, Bottom: {bottom:.3}".format(**_screen_time_stats(sdate)), '##### TIME #####'),
)
