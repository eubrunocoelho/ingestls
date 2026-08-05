import re

GITHUB_URL_PREFIX = 'https://github.com/'

GITHUB_URL_PATTERN = re.compile(
    r'^https://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)/?$'
)

GITHUB_API_BASE_URL = 'https://api.github.com'

DEFAULT_TIMEOUT_SECONDS = 10.0
