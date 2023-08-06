"""API for Bosch API server for Indego lawn mower."""
import asyncio
import inspect
import json
import logging
import typing
import requests

import aiohttp
from aiohttp import (
    ClientResponseError,
    ClientOSError,
    ServerTimeoutError,
    TooManyRedirects,
)
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPGatewayTimeout
from aiohttp.helpers import BasicAuth
from socket import error as SocketError

from . import __version__
from .const import (
    Methods,
    COMMANDS,
    CONTENT_TYPE_JSON,
    DEFAULT_BODY,
    DEFAULT_CALENDAR,
    DEFAULT_HEADER,
    DEFAULT_URL,
)
from .indego_base_client import IndegoBaseClient

_LOGGER = logging.getLogger(__name__)


class IndegoAsyncClient(IndegoBaseClient):
    """Class for Indego Async Client."""

    def __init__(
        self,
        username: str,
        password: str,
        serial: str = None,
        map_filename: str = None,
        api_url: str = DEFAULT_URL,
    ):
        """Initialize the Async Client.

        Args:
            username (str): username for Indego Account
            password (str): password for Indego Account
            serial (str): serial number of the mower
            map_filename (str, optional): Filename to store maps in. Defaults to None.
            api_url (str, optional): url for the api, defaults to DEFAULT_URL.

        """
        super().__init__(username, password, serial, map_filename, api_url)
        self._session = aiohttp.ClientSession(raise_for_status=False)

    async def __aenter__(self):
        """Enter for async with."""
        await self.start()
        return self

    async def __aexit__(self, type, value, traceback):
        """Exit for async with."""
        await self.close()

    async def start(self):
        """Login if not done."""
        if not self._logged_in:
            await self.login()

    async def close(self):
        """Close the aiohttp session."""
        await self._session.close()

    async def delete_alert(self, alert_index: int):
        """Delete the alert with the specified index.

        Args:
            alert_index (int): index of alert to be deleted, should be in range or length of alerts.
            
        """
        alert_id = self._get_alert_by_index(alert_index)
        if alert_id:
            return await self._request(Methods.DELETE, f"alerts/{alert_id}/")
        return None

    async def download_map(self, filename: str = None):
        """Download the map.

        Args:
            filename (str, optional): Filename for the map. Defaults to None, can also be filled by the filename set in init.

        """
        if filename:
            self.map_filename = filename
        if not self.map_filename:
            _LOGGER.error("No map filename defined.")
            return
        map = await self.get(f"alms/{self._serial}/map")
        if map:
            with open(self.map_filename, "wb") as file:
                file.write(map)

    async def patch_alert_read(self, alert_index: int, read_status: bool = True):
        """Set the alert to read.

        Args:
            alert_index (int): index of alert to be deleted, should be in range or length of alerts.
            read_status (bool): new state
            
        """
        alert_id = self._get_alert_by_index(alert_index)
        if alert_id:
            return await self._request(
                Methods.PATCH,
                f"alerts/{alert_id}",
                data={"read_status": "read" if read_status else "unread"},
            )
        return None

    async def put_command(self, command: str):
        """Send a command to the mower.

        Args:
            command (str): command should be one of "mow", "pause", "returnToDock"

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if command in COMMANDS:
            return await self.put(f"alms/{self._serial}/state", {"state": command})
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    async def put_mow_mode(self, command: typing.Any):
        """Set the mower to mode manual (false-ish) or predictive (true-ish).

        Args:
            command (str/bool): should be str that is bool-ish (true, True, false, False) or a bool.

        Returns:
            str: either result of the call or 'Wrong Command'

        """
        if command in ("true", "false", "True", "False") or isinstance(command, bool):
            return await self.put(
                f"alms/{self._serial}/predictive", {"enabled": command}
            )
        _LOGGER.warning("%s not valid", command)
        return "Wrong Command!"

    async def put_predictive_cal(self, calendar: dict = DEFAULT_CALENDAR):
        """Set the predictive calendar."""
        return await self.put(f"alms/{self._serial}/predictive/calendar", calendar)

    async def update_alerts(self):
        """Update alerts."""
        self._update_alerts(await self.get("alerts"))

    async def update_all(self):
        """Update all states."""
        update_list = [
            self.update_alerts(),
            self.update_calendar(),
            self.update_config(),
            self.update_generic_data(),
            self.update_last_completed_mow(),
            self.update_location(),
            self.update_network(),
            self.update_next_mow(),
            self.update_operating_data(),
            self.update_security(),
            self.update_setup(),
            self.update_state(),
            self.update_updates_available(),
            self.update_users(),
        ]
        results = await asyncio.gather(*update_list, return_exceptions=True)
        for res in results:
            if res:
                _LOGGER.warning(res)

    async def update_calendar(self):
        """Update calendar."""
        self._update_calendar(await self.get(f"alms/{self._serial}/calendar"))

    async def update_config(self):
        """Update config."""
        self._update_config(await self.get(f"alms/{self._serial}/config"))

    async def update_generic_data(self):
        """Update generic data."""
        self._update_generic_data(await self.get(f"alms/{self._serial}"))

    async def update_last_completed_mow(self):
        """Update last completed mow."""
        self._update_last_completed_mow(
            await self.get(f"alms/{self._serial}/predictive/lastcutting")
        )

    async def update_location(self):
        """Update location."""
        self._update_location(
            await self.get(f"alms/{self._serial}/predictive/location")
        )

    async def update_network(self):
        """Update network."""
        self._update_network(await self.get(f"alms/{self._serial}/network"))

    async def update_next_mow(self):
        """Update next mow datetime."""
        self._update_next_mow(
            await self.get(f"alms/{self._serial}/predictive/nextcutting")
        )

    async def update_operating_data(self):
        """Update operating data."""
        self._update_operating_data(
            await self.get(f"alms/{self._serial}/operatingData")
        )

    async def update_security(self):
        """Update security."""
        self._update_security(await self.get(f"alms/{self._serial}/security"))

    async def update_setup(self):
        """Update setup."""
        self._update_setup(await self.get(f"alms/{self._serial}/setup"))

    async def update_state(self, force=False, longpoll=False, longpoll_timeout=120):
        """Update state. Can be both forced and with longpoll.

        Args:
            force (bool, optional): Force the state refresh, wakes up the mower. Defaults to False.
            longpoll (bool, optional): Do a longpoll. Defaults to False.
            longpoll_timeout (int, optional): Timeout of the longpoll. Defaults to 120, maximum is 300.

        Raises:
            ValueError: when the longpoll timeout is longer then 300 seconds.

        """
        path = f"alms/{self._serial}/state"
        if longpoll:
            if longpoll_timeout > 300:
                raise ValueError(
                    "Longpoll timeout must be less than or equal 300 seconds."
                )
            last_state = 0
            if self.state.state:
                last_state = self.state.state
            path = f"{path}?longpoll=true&timeout={longpoll_timeout}&last={last_state}"
        if force:
            if longpoll:
                path = f"{path}&forceRefresh=true"
            else:
                path = f"{path}?forceRefresh=true"

        self._update_state(await self.get(path, timeout=longpoll_timeout + 30))

    async def update_updates_available(self):
        """Update updates available."""
        if self._online:
            self._update_updates_available(
                await self.get(f"alms/{self._serial}/updates")
            )

    async def update_users(self):
        """Update users."""
        self._update_users(await self.get(f"users/{self._userid}"))

    async def login(self):
        """Login to the api and store the context."""
        response = await self._request(
            method=Methods.POST,
            path="authenticate",
            data=DEFAULT_BODY,
            headers=DEFAULT_HEADER,
            auth=BasicAuth(self._username, self._password),
            timeout=30,
        )
        self._login(response)
        if response is not None:
            _LOGGER.debug("Logged in")
            if not self._serial:
                list_of_mowers = await self.get("alms")
                self._serial = list_of_mowers[0].get("alm_sn")
                _LOGGER.debug("Serial added")
            return True
        return False

    async def _request(  # noqa: C901
        self,
        method: Methods,
        path: str,
        data: dict = None,
        headers: dict = None,
        auth: BasicAuth = None,
        timeout: int = 30,
        attempts: int = 0,
    ):
        """Request implemented by the subclasses either synchronously or asynchronously.

        Args:
            method (Methods): HTTP method to be executed.
            path (str): url to call on top of base_url.
            data (dict, optional): if applicable, data to be sent, defaults to None.
            headers (dict, optional): headers to be included, defaults to None, which should be filled by the method.
            auth (BasicAuth or HTTPBasicAuth, optional): login specific attribute, defaults to None.
            timeout (int, optional): Timeout for the api call. Defaults to 30.
            attempts (int, optional): Number to keep track of retries, after three starts delaying, after five quites.

        """
        if 3 <= attempts < 5:
            _LOGGER.info("Three or four attempts done, waiting 30 seconds")
            await asyncio.sleep(30)
        if attempts == 5:
            _LOGGER.warning("Five attempts done, please try again later")
            return None
        url = f"{self._api_url}{path}"
        if not headers:
            headers = DEFAULT_HEADER.copy()
            headers["x-im-context-id"] = self._contextid
        try:
            _LOGGER.debug("Sending %s to %s", method.value, url)
            async with self._session.request(
                method=method.value,
                url=url,
                json=data if data else DEFAULT_BODY,
                headers=headers,
                auth=auth,
                timeout=timeout,
            ) as response:
                status = response.status
                if status == 200:
                    # if method in (Methods.DELETE, Methods.PUT, Methods.PATCH):
                    #     return True
                    if response.content_type == CONTENT_TYPE_JSON:
                        return await response.json()
                    return await response.content.read()
                if status == 204:
                    _LOGGER.debug("204: No content in response from server")
                    return None
                if status == 400:
                    _LOGGER.warning(
                        "400: Bad Request: won't retry. Message: %s",
                        (await response.content.read()).decode("UTF-8"),
                    )
                    return None
                if status == 401:
                    if path == "authenticate":
                        _LOGGER.info(
                            "401: Unauthorized, credentials are wrong, won't retry"
                        )
                        return None
                    _LOGGER.info("401: Unauthorized: logging in again")
                    login_result = await self.login()
                    if login_result:
                        return await self._request(
                            method=method,
                            path=path,
                            data=data,
                            timeout=timeout,
                            attempts=attempts + 1,
                        )
                    return None
                if status == 403:
                    _LOGGER.error("403: Forbidden: won't retry")
                    return None
                if status == 405:
                    _LOGGER.error(
                        "405: Method not allowed: %s is used but not allowed, try a different method for path %s, won't retry",
                        method,
                        path,
                    )
                    return None
                if status == 500:
                    _LOGGER.debug("500: Internal Server Error")
                    return None
                if status == 501:
                    _LOGGER.debug("501: Not implemented yet")
                    return None
                if status == 504:
                    if url.find("longpoll=true") > 0:
                        _LOGGER.debug("504: longpoll stopped, no updates")
                        return None
                response.raise_for_status()
        except (asyncio.TimeoutError, ServerTimeoutError, HTTPGatewayTimeout) as e:
            _LOGGER.info("%s: Timeout on Bosch servers, retrying", e)
            return await self._request(
                method=method,
                path=path,
                data=data,
                timeout=timeout,
                attempts=attempts + 1,
            )
        except ClientOSError as e:
            _LOGGER.debug("%s: Failed to update Indego status, longpoll timeout", e)
            return None
        except (TooManyRedirects, ClientResponseError, SocketError) as e:
            _LOGGER.error("%s: Failed %s to Indego, won't retry", e, method.value)
            return None
        except asyncio.CancelledError:
            _LOGGER.debug("Task cancelled by task runner")
            return None
        except Exception as e:
            _LOGGER.error("Request to %s gave a unhandled error: %s", url, e)
            return None

    async def get(self, path: str, timeout: int = 30):
        """Get implemented by the subclasses either synchronously or asynchronously.

        Args:
            path (str): url to call on top of base_url
            timeout (int, optional): Timeout for the api call. Defaults to 30.

        """
        return await self._request(method=Methods.GET, path=path, timeout=timeout)

    async def put(self, path: str, data: dict, timeout: int = 30):
        """Put implemented by the subclasses either synchronously or asynchronously.

        Args:
            path (str): url to call on top of base_url
            data (dict): data to put
            timeout (int, optional): Timeout for the api call. Defaults to 30.

        """
        return await self._request(
            method=Methods.PUT, path=path, data=data, timeout=timeout
        )

    async def post(self, path: str, data: dict, timeout: int = 30):
        """Post implemented by the subclasses either synchronously or asynchronously.

        Args:
            path (str): url to call on top of base_url
            data (dict): data to put
            timeout (int, optional): Timeout for the api call. Defaults to 30.

        """
        return await self._request(
            method=Methods.POST, path=path, data=data, timeout=timeout
        )
