
from ghapi.all import GhApi, paged

api = GhApi(owner='openfast', repo='openfast')

last_release_sha = "ff33ca1cf65f2e13c1de0ab78cc2396ec4a47ce0"

# Find all merged pull requests since the last release
pulls = api.pulls.list(state="closed", per_page=50)
pulls_since = []
for pull in pulls:
    # Is this the pull request corresponding to the last release?
    if pull["merge_commit_sha"] == last_release_sha:
        break

    # skip this loop if the pull request was closed without merge
    if not pull["merge_commit_sha"]:
        continue

    # Otherwise, keep it
    pulls_since.append(pull)

for pull in pulls_since:
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

