
from ghapi.all import GhApi, paged

api = GhApi(owner='openfast', repo='openfast')

# tags = api.repos.list_tags()
# last_release_sha = tags[0].commit.sha
# start_commit = api.git.get_commit(last_release_sha)

# last_release_sha = "ff33ca1cf65f2e13c1de0ab78cc2396ec4a47ce0"

start_commit = api.git.get_commit("42a5a8196529ae0349eda6d797a79461c2c03ff0")
start_date = start_commit.committer.date
stop_commit = api.git.get_commit("a5d6262d62e573dbc8177f6934c336e86dcdba31")
stop_date = stop_commit.committer.date

# Find all merged pull requests in the date range
pulls = api.pulls.list(state="closed", per_page=100)
pulls_since = []
for pull in pulls:
    # print(pull.number)

    # Skip if the pull request was closed without merge
    if pull.merged_at is None:
        continue

    # Skip if this pull request is merged before the last release
    if pull.merged_at <= start_date:
        continue

    # Skip if this pull request is merged after the stop date
    if pull.merged_at > stop_date:
        continue

    # Otherwise, keep it
    pulls_since.append(pull)

pulls_since.sort(key=lambda x: x.merged_at, reverse=True)

for pull in pulls_since:
    # print(pull.number, pull.merged_at, pull.merge_commit_sha)
    labels = [label["name"] for label in pull["labels"]]
    print("#{} {:73s} {}".format(pull["number"], pull["title"], labels))

# 'url', 'id', 'node_id', 'html_url',
# 'diff_url', 'patch_url',
# 'issue_url', 'number',
# 'state', 'locked',
# 'title', 'user',
# 'body',
# 'created_at', 'updated_at', 'closed_at', 'merged_at',
# 'merge_commit_sha',
# 'assignee', 'assignees', 'requested_reviewers', 'requested_teams',
# 'labels', 'milestone',
# 'draft', 'commits_url',
# 'review_comments_url', 'review_comment_url', 'comments_url',
# 'statuses_url',
# 'head', 'base',
# '_links',
# 'author_association',
# 'active_lock_reason'

