import requests

from krules_core.base_functions import *
from krules_core import RuleConst as Const

from krules_core.providers import proc_events_rx_factory
from krules_env import publish_proc_events_errors, publish_proc_events_all  # , publish_proc_events_filtered

try:
    from ruleset_functions import *
except ImportError:
    # for local development
    from .ruleset_functions import *

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

# proc_events_rx_factory().subscribe(
#   on_next=publish_proc_events_all,
# )
proc_events_rx_factory().subscribe(
    on_next=publish_proc_events_errors,
)

rulesdata = [
    """
    On status back to NORMAL notify
    """,
    {
        rulename: "on-temp-status-back-to-normal-slack-notifier",
        subscribe_to: "temp-status-back-to-normal",
        ruledata: {
            processing: [
                Process(
                    lambda self:
                    requests.post(
                        url=self.configs["slack"]["webhooks"]["devices_channel"],
                        json={
                            "type": "mrkdwn",
                            "text": " :sunglasses:  device *{}* temp status back to normal! ".format(
                                self.subject.name)
                        }
                    )
                ),
            ],
        },
    },

    """
    Status COLD or OVERHEATED
    """,
    {
        rulename: "on-temp-status-bad-slack-notifier",
        subscribe_to: "temp-status-bad",
        ruledata: {
            processing: [
                Process(
                    lambda self:
                    requests.post(
                        url=self.configs["slack"]["webhooks"]["devices_channel"],
                        json={
                            "type": "mrkdwn",
                            "text": ":scream:  device *{}* is *{}* ({}°C)".format(
                                self.subject.name, self.payload.get("status"), self.payload.get("tempc")
                            )
                        }
                    )
                ),
            ],
        },
    },

    """
    Notify device status is still bad 
    """,
    {
        rulename: "on-temp-status-recheck-slack-notifier",
        subscribe_to: "temp-status-still-bad",
        ruledata: {
            processing: [
                Process(
                    lambda self:
                    requests.post(
                        url=self.configs["slack"]["webhooks"]["devices_channel"],
                        json={
                            "type": "mrkdwn",
                            "text": ":neutral_face: device *{}* is still *{}* from {} secs".format(
                                self.subject.name,
                                self.payload.get("status"),
                                self.payload.get("seconds")
                            )
                        }
                    )
                ),
            ],
        },
    },
]
