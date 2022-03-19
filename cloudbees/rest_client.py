# coding=utf-8
import logging
from json import dumps

import requests
from six.moves.urllib.parse import urlencode
from requests import HTTPError
from cloudbees.request_utils import get_default_logger

log = get_default_logger(__name__)


class CloudBeesRestAPI(object):
    default_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = None

    def __init__(
        self,
        url,
        username=None,
        password=None,
        timeout=75,
        api_root="rest",
        api_version="v1.0",
        verify_ssl=True,
        session=None,
        cookies=None,
        advanced_mode=None,
        proxies=None,
    ):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self.verify_ssl = verify_ssl
        self.api_root = api_root
        self.api_version = api_version
        self.cookies = cookies
        self.advanced_mode = advanced_mode
        self.proxies = proxies
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        if username and password:
            self._create_basic_session(username, password)
        elif cookies is not None:
            self._session.cookies.update(cookies)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def _create_basic_session(self, username, password):
        self._session.auth = (username, password)

    def _update_header(self, key, value):
        """
        Update header for exist session
        :param key:
        :param value:
        :return:
        """
        self._session.headers.update({key: value})

    @staticmethod
    def _response_handler(response):
        try:
            return response.json()
        except ValueError:
            log.debug("Received response with no content")
            return None
        except Exception as e:
            log.error(e)
            return None

    def log_curl_debug(self, method, url, data=None, headers=None, level=logging.DEBUG):
        """

        :param method:
        :param url:
        :param data:
        :param headers:
        :param level:
        :return:
        """
        headers = headers or self.default_headers
        message = "curl --silent -X {method} -H {headers} {data} '{url}'".format(
            method=method,
            headers=" -H ".join(["'{0}: {1}'".format(key, value) for key, value in headers.items()]),
            data="" if not data else "--data '{0}'".format(dumps(data)),
            url=url,
        )
        log.log(level=level, msg=message)

    def resource_url(self, resource, api_root=None, api_version=None):
        if api_root is None:
            api_root = self.api_root
        if api_version is None:
            api_version = self.api_version
        return "/".join(s.strip("/") for s in [api_root, api_version, resource] if s is not None)

    @staticmethod
    def url_joiner(url, path, trailing=None):
        url_link = "/".join(str(s).strip("/") for s in [url, path] if s is not None)
        if trailing:
            url_link += "/"
        return url_link

    def close(self):
        return self._session.close()

    def request(
        self,
        method="GET",
        path="/",
        data=None,
        json=None,
        flags=None,
        params=None,
        headers=None,
        files=None,
        trailing=None,
        absolute=False,
    ):
        """

        :param method:
        :param path:
        :param data:
        :param json:
        :param flags:
        :param params:
        :param headers:
        :param files:
        :param trailing: bool
        :param absolute: bool, OPTIONAL: Do not prefix url, url is absolute
        :return:
        """
        url = self.url_joiner(None if absolute else self.url, path, trailing)
        params_already_in_url = True if "?" in url else False
        if params or flags:
            if params_already_in_url:
                url += "&"
            else:
                url += "?"
        if params:
            url += urlencode(params or {})
        if flags:
            url += ("&" if params or params_already_in_url else "") + "&".join(flags or [])
        json_dump = None
        if files is None:
            data = None if not data else dumps(data)
            json_dump = None if not json else dumps(json)
        self.log_curl_debug(method=method, url=url, headers=headers, data=data if data else json_dump)
        headers = headers or self.default_headers
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            json=json,
            timeout=self.timeout,
            verify=self.verify_ssl,
            files=files,
            proxies=self.proxies,
        )
        response.encoding = "utf-8"

        log.debug("HTTP: {} {} -> {} {}".format(method, path, response.status_code, response.reason))
        log.debug("HTTP: Response text -> {}".format(response.text))
        if self.advanced_mode:
            return response

        self.raise_for_status(response)
        return response

    def get(
        self,
        path,
        data=None,
        flags=None,
        params=None,
        headers=None,
        not_json_response=None,
        trailing=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        Get request based on the python-requests module. You can override headers, and also, get not json response
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw requests packet
        :param trailing: OPTIONAL: for wrap slash symbol in the end of string
        :param absolute: bool, OPTIONAL: Do not prefix url, url is absolute
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return:
        """
        response = self.request(
            "GET",
            path=path,
            flags=flags,
            params=params,
            data=data,
            headers=headers,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        if not_json_response:
            return response.content
        else:
            if not response.text:
                return None
            try:
                return response.json()
            except Exception as e:
                log.error(e)
                return response.text

    def post(
        self,
        path,
        data=None,
        json=None,
        headers=None,
        files=None,
        params=None,
        trailing=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return: if advanced_mode is not set - returns dictionary. If it is set - returns raw response.
        """
        response = self.request(
            "POST",
            path=path,
            data=data,
            json=json,
            headers=headers,
            files=files,
            params=params,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    def put(
        self,
        path,
        data=None,
        headers=None,
        files=None,
        trailing=None,
        params=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :return: if advanced_mode is not set - returns dictionary. If it is set - returns raw response.
        """
        response = self.request(
            "PUT",
            path=path,
            data=data,
            headers=headers,
            files=files,
            params=params,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    def delete(
        self,
        path,
        data=None,
        headers=None,
        params=None,
        trailing=None,
        absolute=False,
        advanced_mode=False,
    ):
        """
        Deletes resources at given paths.
        :param advanced_mode: bool, OPTIONAL: Return the raw response
        :rtype: dict
        :return: Empty dictionary to have consistent interface.
        Some of CloudBees REST resources don't return any content.
        If advanced_mode is set - returns raw response.
        """
        response = self.request(
            "DELETE",
            path=path,
            data=data,
            headers=headers,
            params=params,
            trailing=trailing,
            absolute=absolute,
        )
        if self.advanced_mode or advanced_mode:
            return response
        return self._response_handler(response)

    def raise_for_status(self, response):
        """
        Checks the response for errors and throws an exception if return code >= 400
        Since different tools have different formats of returned json,
        this method is intended to be overwritten by a tool specific implementation.
        :param response:
        :return:
        """
        if 400 <= response.status_code < 600:
            try:
                j = response.json()
                error_msg = "\n".join(j["errorMessages"] + [k + ": " + v for k, v in j["errors"].items()])
            except Exception:
                response.raise_for_status()
            else:
                raise HTTPError(error_msg, response=response)
        else:
            response.raise_for_status()
