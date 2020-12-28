Using docsclient
****************

``docsclient`` is used to upload documentation to |docserver| :github:`djpugh/docserver`. It provides a
simple python object that can be used to connect and upload documentation folders/zip files.

It uses an ``authenticator`` object that can provide token/session authentication for the client,
or can be a simple bearer token string.


Including docsclient in your code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


You can use it from python::

    from docsclient import AADAuthentication, Client

    client = Client('<my-host-url>', authenticator=AADAuthentication())

    client.upload_dir('./docs/html', '<my-module-name>', __version__, '<my-repo-url>', tags=['python', 'demo'])

This uses |aad_client| :github:`djpugh/aad_client` for authentication, which uses several environment variables.
This assumes that your |docserver| :github:`djpugh/docserver` instance is running with Azure Active Directory
Authentication configured.

Authenticating a client
~~~~~~~~~~~~~~~~~~~~~~~

The authentication approach is pretty simple. You can either provide a token in the :py:obj:`~aad_client.Client` init
as the ``authenticator`` argument (as a string) - it needs to just be the token, and it will be converted to the correct
format.

Alternatively, you can provide an ``authenticator`` object (e.g. :py:obj:`aad_client.AADAuthentication` from |aad_client| :github:`djpugh/aad_client`).
This should provide either a ``headers`` attribute containing the headers with the authentication, or a ``session`` attribute, returning a
:py:obj:`requests.sessions.Session` type object, with authentication headers.

The authentication method needs to match that used in the |docserver| :github:`djpugh/docserver` configuration.
