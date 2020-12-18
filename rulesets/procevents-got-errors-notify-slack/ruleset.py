
from krules_core.base_functions import *
from krules_core import RuleConst as Const
import requests
import jsonpath_rw_ext as jp

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

from krules_core.providers import proc_events_rx_factory
from krules_env import RULE_PROC_EVENT


rulesdata = [
    """
    Send processed events errors to Slack
    """,
    {
        rulename: "on-procevents-error-notify-slack",
        subscribe_to: [RULE_PROC_EVENT],
        ruledata: {
            filters: [
                Filter(lambda payload: payload["got_errors"])
            ],
            processing: [
                SetPayloadProperty("key", 2),
                Process(
                    lambda self:
                        requests.post(
                            url=self.configs["slack"]["webhooks"]["errors"],
                            json={
                                "type": "mrkdwn",
                                "text":
                                    ":ambulance: *{}[{}]* \n```\n{}\n```".format(
                                        self.subject.event_info()["source"],
                                        self.payload["name"],
                                        "\n".join(jp.match1("$.processing[*].exc_info", self.payload))
                                    )
                            }
                        )
                )
            ]
        }
    },
]

