import pprint
import hashlib
import requests
from krules_core.base_functions.misc import PyCall


def hashed(name, *args, length=10):
    hash = ""
    for arg in args:
        hash += pprint.pformat(arg)
    return "{}-{}".format(name, hashlib.md5(hash.encode("utf8")).hexdigest()[:length])


class DoRestApiCall(PyCall):

    def _do_request(self, path, method, json):

        self.payload["__json"] = json
        req_kwargs = {
            "url": "{}{}".format(
                self.configs["django"]["restapi"]["url"],
                path
            ),
            "headers": {"Authorization": "Token %s" % self.configs["django"]["restapi"]["api_key"]},
        }
        if method != "get":
            req_kwargs["json"] = json

        resp = getattr(requests, method)(
            **req_kwargs
        )
        resp.raise_for_status()
        return resp

    def execute(self, path, method="post", json=None, **kwargs):

        if json is None:
            json = {}

        super().execute(
            self._do_request,
            kwargs={
                "path": path,
                "method": method,
                "json": json
            },
            **kwargs
        )


class DoPostApiCall(DoRestApiCall):

    def execute(self, path, json=None, **kwargs):

        super().execute(path, method="post", json=json, **kwargs)


class DoPatchApiCall(DoRestApiCall):

    def execute(self, path, json=None, **kwargs):

        super().execute(path, method="patch", json=json, **kwargs)


class DoPutApiCall(DoRestApiCall):

    def execute(self, path, json=None, **kwargs):

        super().execute(path, method="put", json=json, **kwargs)


class DoGetApiCall(DoRestApiCall):

    def execute(self, path, **kwargs):

        super().execute(path, method="get", json=None, **kwargs)
