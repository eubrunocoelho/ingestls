import re

GITHUB_URL_PREFIX = 'https://github.com/'

GITHUB_URL_PATTERN = re.compile(
    r'^https://github\.com/'
    r'(?P<owner>[\w.-]+)/'
    r'(?P<repo>[\w.-]+)'
    r'(?:/tree/(?P<reference>[^/]+)(?:/(?P<path>.*))?)?'
    r'/?$'
)
