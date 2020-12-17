
from krules_core.base_functions import *
from krules_core import RuleConst as Const
import requests
from datetime import datetime

from krules_core.providers import configs_factory

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

from krules_core.providers import proc_events_rx_factory
from krules_env import publish_proc_events_errors, RULE_PROC_EVENT

proc_events_rx_factory().subscribe(
 on_next=publish_proc_events_errors,
)

rulesdata = [
    """
    Store rules metrics in Django ORM
    """,
    {
        rulename: "django-orm-store-full-data",
        subscribe_to: RULE_PROC_EVENT,
        ruledata: {
            processing: [
                PyCall(
                    requests.post,
                    kwargs=lambda payload:{
                        "url": configs_factory()["django"]["restapi_auth"]["url"],
                        "headers": {"Authentication": "Token %s" % configs_factory()["django"]["restapi_auth"]["api_key"]},
                        "json": {
                            "rule_name": payload["name"],
                            "type": payload["type"],
                            "subject": payload["subject"],
                            "event_info": payload["event_info"],
                            "payload": payload["payload"],
                            "time": payload["event_info"].get("time", datetime.now().isoformat()),
                            "filters": payload["filters"],
                            "processing": payload["processing"],
                            "got_errors": payload["got_errors"],
                            "processed": payload["processed"],
                            "origin_id": payload["event_info"].get("originid", "-")
                        }
                    }
                )
            ],
        },
    },
]

