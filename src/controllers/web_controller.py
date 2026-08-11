from flask import Response

from src.providers.view.view_provider import ViewProvider


class WebController:
    def __init__(
            self,
            view_provider: ViewProvider,
    ):
        self.view_provider = view_provider

    def index(self) -> Response:
        return Response(
            self.view_provider.render('index.html'),
            mimetype='text/html',
        )
