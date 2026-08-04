from html import escape
from pprint import pformat


class DebugResponse:
    @staticmethod
    def to_html(value) -> str:
        return f'''
        <pre>{escape(pformat(value, sort_dicts=False))}</pre>
        '''
