from __future__ import absolute_import

import requests
import json

from .exceptions import StorageServerException
from .models import HttpOptions, HttpRecordRead, HttpRecordFind
from .validation import validate_http_response
from .__version__ import __version__


class HttpClient:
    PORTALBACKEND_URI = "https://portal-backend.incountry.com"
    DEFAULT_ENDPOINT = "https://us.api.incountry.io"

    def __init__(self, env_id, api_key, endpoint=None, debug=False, options={}):
        self.api_key = api_key
        self.endpoint = endpoint
        self.env_id = env_id
        self.debug = debug
        self.options = HttpOptions(**options)

        if self.endpoint is None:
            self.log(
                f"Connecting to default endpoint: https://<country>.api.incountry.io. "
                f"Connection timeout {self.options.timeout}s"
            )
        else:
            self.log(f"Connecting to custom endpoint: {self.endpoint}. Connection timeout {self.options.timeout}s")

    def write(self, country, data):
        response = self.request(country, method="POST", data=json.dumps(data))
        return response

    def batch_write(self, country, data):
        response = self.request(country, path="/batchWrite", method="POST", data=json.dumps(data))
        return response

    @validate_http_response(HttpRecordRead)
    def read(self, country, key):
        response = self.request(country, path="/" + key)
        return response

    @validate_http_response(HttpRecordFind)
    def find(self, country, data):
        response = self.request(country, path="/find", method="POST", data=json.dumps(data))
        return response

    def delete(self, country, key):
        return self.request(country, path="/" + key, method="DELETE")

    def request(self, country, path="", method="GET", data=None):
        try:
            endpoint = self.getendpoint(country, "/v2/storage/records/" + country + path)
            res = requests.request(
                method=method, url=endpoint, headers=self.get_headers(), data=data, timeout=self.options.timeout
            )

            if res.status_code >= 400:
                raise StorageServerException("{} {} - {}".format(res.status_code, res.url, res.text))

            try:
                return res.json()
            except Exception:
                return res.text
        except Exception as e:
            raise StorageServerException(e) from None

    def get_midpop_country_codes(self):
        r = requests.get(self.PORTALBACKEND_URI + "/countries", timeout=self.options.timeout)
        if r.status_code >= 400:
            raise StorageServerException("Unable to retrieve countries list")
        data = r.json()

        return [country["id"].lower() for country in data["countries"] if country["direct"]]

    def getendpoint(self, country, path):
        if not path.startswith("/"):
            path = "/" + path

        if self.endpoint:
            res = "{}{}".format(self.endpoint, path)
            self.log("Endpoint: ", res)
            return res

        midpops = self.get_midpop_country_codes()

        is_midpop = country in midpops

        res = HttpClient.get_midpop_url(country) + path if is_midpop else "{}{}".format(self.DEFAULT_ENDPOINT, path)

        self.log("Endpoint: ", res)
        return res

    def get_headers(self):
        return {
            "Authorization": "Bearer " + self.api_key,
            "x-env-id": self.env_id,
            "Content-Type": "application/json",
            "User-Agent": "SDK-Python/" + __version__,
        }

    def log(self, *args):
        if self.debug:
            print("[incountry] ", args)

    @staticmethod
    def get_midpop_url(country):
        return "https://{}.api.incountry.io".format(country)
