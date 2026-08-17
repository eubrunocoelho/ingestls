import re

GITHUB_URL_PREFIX = 'https://github.com/'

GITHUB_URL_PATTERN = re.compile(
    r'^https://github\.com/'
    r'[\w.-]+/'  # owner
    r'[\w.-]+'  # repo
    r'(?:/tree/.+)?'  # opcional: /tree/<referencia>[/<path>...]
    r'/?$'
)
