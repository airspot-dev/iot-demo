from datetime import datetime, timezone
import requests

from krules_core.base_functions import RuleFunctionBase
from providers import subject_factory


class DispatchScheduledEvents(RuleFunctionBase):

    def execute(self):
        headers = {"Authorization": "Token %s" % self.configs["django"]["restapi"]["api_key"]}
        url = "%s/scheduler/scheduled_event?when__lte=%s" % (
                self.configs["django"]["restapi"]["url"], datetime.now(timezone.utc).isoformat())
        response = requests.get(
            url=url.replace("+", "%2B"),
            headers=headers

        )
        response.raise_for_status()
        for event in response.json():
            sub = subject_factory(event["subject"])
            self.router.route(event["event_type"], sub, event["payload"])
            resp = requests.delete(
                url="%s/scheduler/scheduled_event/%s" %
                    (self.configs["django"]["restapi"]["url"], event["uid"]),
                headers=headers
            )
            resp.raise_for_status()
            sub.set("schedule_status_uid", None, muted=True)


def call_to_api(url, method, headers, **kwargs):
    resp = eval("requests.%s" % method)(url, headers=headers, **kwargs)
    resp.raise_for_status()
    return resp.json()
