import requests
from krules_core.base_functions import RuleFunctionBase
from datetime import datetime


class DispatchScheduledEvents(RuleFunctionBase):

    def execute(self):
        headers = {"Authorization": "Token %s" % self.configs["django"]["restapi"]["api_key"]}
        response = requests.get(
            url="%s/scheduler/scheduled_event?when__lte=%s" % (
                self.configs["django"]["restapi"]["url"], datetime.now().isoformat()),
            headers=headers

        )
        response.raise_for_status()
        for event in response.json():
            self.router.route(event["event_type"], event["subject"], event["payload"])
            resp = requests.delete(
                url="%s/scheduler/scheduled_event/%s" %
                    (self.configs["django"]["restapi"]["url"], event["uid"]),
                headers=headers
            )
            resp.raise_for_status()


def call_to_api(url, method, headers, **kwargs):
    resp = eval("requests.%s" % method)(url, headers=headers, **kwargs)
    resp.raise_for_status()
    return resp.json()
