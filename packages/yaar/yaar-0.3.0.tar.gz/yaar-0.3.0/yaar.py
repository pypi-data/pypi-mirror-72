# -*- coding: utf-8 -*-
"""This module implements a simple asynchronous interface for
http requests.

Usage:
``````

.. code-block:: python

    import yaar
    response = await yaar.get('http://google.com/')
    print(response.text)
"""

# Copyright 2019 Juca Crispim <juca@poraodojuca.net>

# This file is part of yaar.

# yaar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# yaar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with yaar. If not, see <http://www.gnu.org/licenses/>.

import asyncio
import json
import aiohttp


VERSION = '0.3.0'


class HTTPRequestError(Exception):
    pass


class Response:
    """Encapsulates a response from a http request"""

    def __init__(self, status, content):
        """Constructor for Response.

        :param status: The response status.
        :param content: The response content as bytes."""
        self.status = status
        self.content = content
        self._text = None

    @property
    def text(self):
        if self._text is not None:  # pragma no cover
            return self._text
        self._text = self.content.decode()
        return self._text

    def json(self):
        """Loads the json in the response text."""

        return json.loads(self.text)


async def _request(method, url, session=None, **kwargs):
    """Performs a http request and returns an instance of
    :class:`yaar.core.requests.Response`

    :param method: The requrest's method.
    :param session: An aiohttp.ClientSession instance. If None a new one will
      be created.
    :param url: Request's url.
    :param kwargs: Arguments passed to aiohttp.ClientSession.request
        method.
    """

    loop = asyncio.get_event_loop()

    client = session or aiohttp.ClientSession(loop=loop)
    try:
        resp = await client.request(method, url, **kwargs)
        status = resp.status
        content = await resp.read()
        await resp.release()
    finally:
        await client.close()

    r = Response(status, content)
    if r.status >= 400:
        raise HTTPRequestError(r.status, r.text)
    return r


async def get(url, session=None, **kwargs):
    """Performs a http GET request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'GET'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def post(url, session=None, **kwargs):
    """Performs a http POST request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'POST'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def put(url, session=None, **kwargs):
    """Performs a http PUT request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'PUT'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def delete(url, session=None, **kwargs):
    """Performs a http DELETE request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'DELETE'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def patch(url, session=None, **kwargs):
    """Performs a http PATCH request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'PATCH'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def options(url, session=None, **kwargs):
    """Performs a http OPTIONS request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'OPTIONS'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def head(url, session=None, **kwargs):
    """Performs a http HEAD request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'HEAD'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def connect(url, session=None, **kwargs):
    """Performs a http CONNECT request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'CONNECT'
    resp = await _request(method, url, session=session, **kwargs)
    return resp


async def trace(url, session=None, **kwargs):
    """Performs a http TRACE request

    :param url: Request's url.
    :param session: Session passed to :func:`yaar.core.requests._request`.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'TRACE'
    resp = await _request(method, url, session=session, **kwargs)
    return resp
