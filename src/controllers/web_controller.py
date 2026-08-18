from flask import Response

from src.providers.jinja_view_provider import JinjaViewProvider


class WebController:
    def __init__(
            self,
            view_provider: JinjaViewProvider,
    ):
        self.view_provider = view_provider

    def index(self) -> Response:
        return Response(
            self.view_provider.render('index.html'),
            mimetype='text/html',
        )
