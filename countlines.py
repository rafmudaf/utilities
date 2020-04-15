
from git import Repo
from subprocess import Popen, PIPE
import time
# git log --format=%H

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


repo = Repo('floris')
git = repo.git

commit_index = []
line_count = []
commit_dates = []

commit_list = list(repo.iter_commits('develop', max_count=1032))

for index, commit in enumerate(commit_list):

    git.checkout(commit)

    p1 = Popen(
        [
            'find',
            '.',
            '-name',
            '*.py',
            '-print0'
        ],
        stdout=PIPE
    )

    p2 = Popen(
        [
            "xargs",
            "-0",
            "cat"
        ],
        stdin=p1.stdout,
        stdout=PIPE
    )

    p3 = Popen(
        [
            "wc",
            "-l"
        ],
        stdin=p2.stdout,
        stdout=PIPE
    )

    output, error = p3.communicate()

    if error is not None:
        print(error)
        raise Exception

    output = int(output.decode().strip())

    line_count.append(output)
    commit_index.append(index)

    # commit_date = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(repo.head.commit.committed_date))
    commit_date = time.strftime('%Y-%m-%d', time.gmtime(repo.head.commit.committed_date))

    commit_dates.append(commit_date)

    del p1, p2, p3, output

line_count.reverse()
commit_dates.reverse()

plt.figure()
plt.plot(commit_index, line_count)
plt.show()


# years = mdates.YearLocator()   # every year
# months = mdates.MonthLocator()  # every month
# years_fmt = mdates.DateFormatter('%Y')

# fig, ax = plt.subplots()
# ax.plot(commit_dates, line_count)

# # format the ticks
# ax.xaxis.set_major_locator(years)
# ax.xaxis.set_major_formatter(years_fmt)
# ax.xaxis.set_minor_locator(months)

# # round to nearest years.
# datemin = np.datetime64('2017')
# datemax = np.datetime64('2020')
# ax.set_xlim(str(datemin), str(datemax))

# # format the coords message box
# ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# # ax.grid(True)

# # rotates and right aligns the x labels, and moves the bottom of the
# # axes up to make room for them
# fig.autofmt_xdate()

# plt.show()
