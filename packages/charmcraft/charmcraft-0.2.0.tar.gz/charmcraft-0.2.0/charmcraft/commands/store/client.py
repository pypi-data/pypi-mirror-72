# Copyright 2020 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft

"""A client to hit the Store."""

import logging
import os
import webbrowser
from http.cookiejar import MozillaCookieJar

import appdirs
from macaroonbakery import httpbakery

from charmcraft.cmdbase import CommandError

logger = logging.getLogger('charmcraft.commands.store')

# XXX Facundo 2020-06-19: only staging for now; will make it "multi-server" when we have proper
# functionality in Store's production (related: issue #51)
BASE_URL = 'https://api.staging.snapcraft.io/publisher/api'


def visit_page_with_browser(visit_url):
    """Open a browser so the user can validate its identity."""
    logger.warning(
        "Opening an authorization web page in your browser; if it does not open, "
        "please open this URL: %s", visit_url)
    webbrowser.open(visit_url, new=1)


class _AuthHolder:
    """Holder and wrapper of all authentication bits.

    Main two purposes of this class:

    - deal with credentials persistence

    - wrap HTTP calls to ensure authentication

    XXX Facundo 2020-06-18: right now for functionality bootstrapping we're storing credentials
    on disk, we may move to a keyring, wallet, other solution, or firmly remain here when we
    get a "security" recommendation (related: issue #52).
    """

    def __init__(self):
        self._cookiejar_filepath = appdirs.user_config_dir('charmcraft.credentials')
        self._cookiejar = None
        self._client = None

    def clear_credentials(self):
        """Clear stored credentials."""
        if os.path.exists(self._cookiejar_filepath):
            os.unlink(self._cookiejar_filepath)
            logger.debug("Credentials cleared: file %r removed", self._cookiejar_filepath)
        else:
            logger.debug("Credentials file not found to be removed: %r", self._cookiejar_filepath)

    def _save_credentials_if_changed(self):
        """Save credentials if changed."""
        if list(self._cookiejar) != self._old_cookies:
            logger.debug("Saving credentials to file: %r", self._cookiejar_filepath)
            dirpath = os.path.dirname(self._cookiejar_filepath)
            os.makedirs(dirpath, exist_ok=True)

            self._cookiejar.save()

    def _load_credentials(self):
        """Load credentials and set up internal auth request objects."""
        wbi = httpbakery.WebBrowserInteractor(open=visit_page_with_browser)
        self._cookiejar = MozillaCookieJar(self._cookiejar_filepath)
        self._client = httpbakery.Client(cookies=self._cookiejar, interaction_methods=[wbi])

        if os.path.exists(self._cookiejar_filepath):
            logger.debug("Loading credentials from file: %r", self._cookiejar_filepath)
            try:
                self._cookiejar.load()
            except Exception as err:
                # alert and continue processing (without having credentials, of course, the user
                # will be asked to authenticate)
                logger.warning("Failed to read credentials: %r", err)
        else:
            logger.debug("Credentials file not found: %r", self._cookiejar_filepath)

        # iterates the cookiejar (which is mutable, may change later) and get the cookies
        # for comparison after hitting the endpoint
        self._old_cookies = list(self._cookiejar)

    def request(self, method, url):
        """Do a request."""
        if self._client is None:
            # load everything on first usage
            self._load_credentials()

        # this request through the bakery lib will automatically catch any authentication
        # problem and (if any) ask the user to authenticate and retry the original request; if
        # that fails we capture it and raise a proper error
        try:
            resp = self._client.request(method, url)
        except httpbakery.InteractionError as err:
            raise CommandError("Authentication failure: {}".format(err))

        self._save_credentials_if_changed()
        return resp


class Client:
    """Lightweight layer above _AuthHolder to present a more network oriented interface."""

    def __init__(self):
        self._auth_client = _AuthHolder()

    def clear_credentials(self):
        """Clear stored credentials."""
        self._auth_client.clear_credentials()

    def _hit(self, method, urlpath):
        """Generic hit to the Store."""
        url = BASE_URL + urlpath
        logger.debug("Hitting the store: %s %s", method, url)
        resp = self._auth_client.request(method, url)
        if not resp.ok:
            raise CommandError(
                "Failure working with the Store: [{}] {!r}".format(resp.status_code, resp.content))

        data = resp.json()
        return data

    def get(self, urlpath):
        """GET something from the Store."""
        return self._hit('GET', urlpath)
