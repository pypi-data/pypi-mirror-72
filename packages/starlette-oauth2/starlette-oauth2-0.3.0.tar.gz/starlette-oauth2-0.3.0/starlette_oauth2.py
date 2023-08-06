import typing
import logging

from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send
from authlib.integrations.starlette_client import StarletteRemoteApp, StartletteIntegration


logger = logging.getLogger(__name__)


class AuthenticateMiddleware:
    REDIRECT_PATH = '/authorized'

    # set of public paths (paths that do not need authentication)
    PUBLIC_PATHS = set()

    def __init__(self,
        app: ASGIApp,
        server_metadata_url: str,
        client_id: str,
        client_secret: str,
        db=None,
        force_https_redirect=True) -> None:
        self.app = app
        self.db = db
        self._force_https_redirect = force_https_redirect

        self._client = StarletteRemoteApp(
            StartletteIntegration('starlette'),
            client_id=str(client_id),
            client_secret=str(client_secret),
            server_metadata_url=server_metadata_url,
            client_kwargs={'scope': 'openid email profile'},
        )

    def _redirect_uri(self, request: Request):
        """
        The URI of the redirect path. This should be registered on whatever provider is declared.
        """
        port = request.url.port
        if port is None:
            port = ''
        else:
            port = ':' + str(port)
        scheme = request.url.scheme
        if scheme == 'http' and self._force_https_redirect:
            scheme = 'https'
        return f"{scheme}://{request.url.hostname}{port}{self.REDIRECT_PATH}"

    async def _authenticate(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope)

        logger.info(f'Authenticating a user arriving at "{request.url.path}"')

        if request.url.path != self.REDIRECT_PATH:
            # store the original path of the request to redirect to when the user authenticates
            request.session['original_path'] = str(request.url)

            # any un-authenticated request is redirected to the tenant
            redirect_uri = self._redirect_uri(request)
            response = await self._client.authorize_redirect(request, redirect_uri)
            await response(scope, receive, send)
        else:
            logger.info(f'Fetching id token...')
            # try to construct a user from the access token
            try:
                token = await self._client.authorize_access_token(request)
                user = await self._client.parse_id_token(request, token)
                assert user is not None
            except Exception as e:
                # impossible to build a user => invalidate the whole thing and redirect to home (which triggers a new auth)
                logger.error('User authentication failed', exc_info=True)
                response = RedirectResponse(url='/')
                await response(scope, receive, send)
                return

            # store token id and access token
            request.session['user'] = dict(user)

            logger.info(f'Storing access token of user "{user["email"]}"...')
            if self.db is None:
                request.session['token'] = dict(token)
            else:
                self.db.put(user['email'], dict(token))

            # finally, redirect to the original path
            path = request.session.pop('original_path')

            response = RedirectResponse(url=path)
            await response(scope, receive, send)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope)

        if request.url.path in self.PUBLIC_PATHS:
            return await self.app(scope, receive, send)

        user = request.session.get('user')

        # no user => start authentication
        if user is None:
            return await self._authenticate(scope, receive, send)

        # fetch the token from the database associated with the user
        if self.db is None:
            token = request.session.get('token')
        else:
            token = self.db.get(user['email'])

        try:
            # check that the token is still valid (e.g. it has not expired)
            if token is None:
                raise errors.InvalidTokenError
            await self._client.parse_id_token(request, token)
        except Exception as e:
            # invalidate session and redirect.
            del request.session['user']
            if self.db is None:
                del request.session['token']
            else:
                self.db.delete(user['email'])

            redirect_uri = self._redirect_uri(request)
            response = self._client.authorize_redirect(request, redirect_uri)
            return await response(scope, receive, send)

        logger.info(f'User "{user["email"]}" is authenticated.')

        await self.app(scope, receive, send)


__all__ = ['AuthenticateMiddleware']
