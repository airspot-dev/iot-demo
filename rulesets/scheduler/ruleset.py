from pprint import pprint

from krules_core.base_functions.misc import PyCall
from krules_core.base_functions import *
from krules_core import RuleConst as Const
import requests
from datetime import datetime
from ruleset_functions import DispatchScheduledEvents, call_to_api

#
# try:
#     from ruleset_functions import *
# except ImportError:
#     # for local development
#     from .ruleset_functions import *

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

from krules_core.providers import proc_events_rx_factory, subject_factory
from krules_env import publish_proc_events_errors, publish_proc_events_all  # , publish_proc_events_filtered

proc_events_rx_factory().subscribe(
    on_next=pprint,
)
# proc_events_rx_factory().subscribe(
#     on_next=publish_proc_events_errors,
# )

rulesdata = [
    """
    Store schedule info (no replace)
    """,
    {
        rulename: "on-schedule-received-no-replace",
        subscribe_to: "schedule-message",
        ruledata: {
            filters: [
                Filter(lambda payload: not payload.get("replace", False))
            ],
            processing: [
                PyCall(
                    call_to_api,
                    kwargs=lambda self: {
                        "url": "%s/scheduler/scheduled_event/" % self.configs["django"]["restapi"]["url"],
                        "headers": {"Authorization": "Token %s" % self.configs["django"]["restapi"]["api_key"]},
                        "json": {
                            "event_type": self.payload["event_type"],
                            "subject": self.payload["subject"],
                            "payload": self.payload["payload"],
                            "origin_id": self.payload["origin_id"],
                            "when": self.payload["when"],
                        }
                    }
                ),
                Process(
                    lambda self:
                    requests.post(
                        url="%s/scheduler/scheduled_event/" % self.configs["django"]["restapi"]["url"],
                        headers={"Authorization": "Token %s" % self.configs["django"]["restapi"]["api_key"]},
                        json={
                            "event_type": self.payload["event_type"],
                            "subject": self.payload["subject"],
                            "payload": self.payload["payload"],
                            "origin_id": self.payload["origin_id"],
                            "when": self.payload["when"],
                        }
                    )
                )
            ]
        }
    },
    """
    Update schedule info (replace)
    """,
    {
        rulename: "on-schedule-received-replace",
        subscribe_to: "schedule-message",
        ruledata: {
            filters: [
                Filter(lambda payload: payload.get("replace", True))
            ],
            processing: [
                Process(
                    lambda self:
                    requests.put(
                        url="%s/scheduler/scheduled_event/%s" %
                            (self.configs["django"]["restapi"]["url"], self.payload["uid"]),
                        headers={"Authorization": "Token %s" % self.configs["django"]["restapi"]["api_key"]},
                        json={
                            "payload": self.payload["payload"],
                            "when": self.payload["when"],
                        }
                    )
                )
            ]
        }
    },
    """
    On tick route scheduled events
    """,
    {
        rulename: "on-tick-do-schedules",
        subscribe_to: "krules.heartbeat",
        ruledata: {
            processing: [
                DispatchScheduledEvents()
            ]
        }
    },
]
