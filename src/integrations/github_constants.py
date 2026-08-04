import re

GITHUB_URL_PREFIX = 'https://github.com/'

GITHUB_URL_PATTERN = re.compile(
    r'^https://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)/?$'
)
