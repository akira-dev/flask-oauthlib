# coding: utf-8
"""
    flask_oauthlib.provider
    ~~~~~~~~~~~~~~~~~~~~~~~

    Implemnts OAuth2 provider support for Flask.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

from flask import request
from flask import _app_ctx_stack


class OAuth(object):
    """Provide secure services using OAuth2.

    The server should provide an authorize handler, access token hander,
    refresh token hander::

        @oauth.clientgetter
        def client(client_id):
            client = get_client(client_id)
            # Client is an object
            return client

        @app.route('/oauth/authorize', methods=['GET', 'POST'])
        @app.authorize_handler
        def authorize(client_id, response_type,
                      redirect_uri, scopes, **kwargs):
            return render_template('oauthorize.html')

        @app.route('/oauth/access_token')
        @app.access_token_handler
        def access_token(client):
            # maybe you need a record
            return {}

        @app.route('/oauth/access_token')
        @app.refresh_token_handler
        def refresh_token(client):
            # maybe you need a record
            return {}

    Protect the resource with scopes::

        @app.route('/api/user')
        @oauth.require_oauth(['email'])
        def user():
            return jsonify(g.user)
    """

    def __init__(self, app=None):
        self._client_getter = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['oauth-provider'] = self

    def get_app(self):
        if self.app is not None:
            return self.app
        ctx = _app_ctx_stack.top
        if ctx is not None:
            return ctx.app
        raise RuntimeError(
            'application not registered on Oauth '
            'instance and no application bound to current context'
        )

    def access_token_methods(self):
        app = self.get_app()
        methods = app.config.get('OAUTH_ACCESS_TOKEN_METHODS', ['POST'])
        if isinstance(methods, (list, tuple)):
            return methods
        return [methods]

    def clientgetter(self, f):
        self._client_getter = f

    def authorize_handler(self, func):
        pass

    def access_token_handler(self, func):
        if request.method not in self.access_token_methods():
            # method invalid
            pass

    def refresh_token_handler(self, func):
        pass

    def require_oauth(self, scope=None):
        pass