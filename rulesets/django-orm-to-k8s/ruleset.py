import base64

from krules_core.base_functions import *
from krules_core import RuleConst as Const

rulename = Const.RULENAME
subscribe_to = Const.SUBSCRIBE_TO
ruledata = Const.RULEDATA
filters = Const.FILTERS
processing = Const.PROCESSING

from krules_core.providers import proc_events_rx_factory
from krules_env import publish_proc_events_errors, publish_proc_events_all  # , publish_proc_events_filtered

proc_events_rx_factory().subscribe(
    on_next=publish_proc_events_all,
)
# proc_events_rx_factory().subscribe(
#  on_next=publish_proc_events_errors,
# )
from app_functions import hashed
from k8s_functions import K8sObjectCreate, K8sObjectsQuery

try:
    from ruleset_functions import *
except ImportError:
    # for local development
    from .ruleset_functions import *

IMAGE_DIGEST = 'lorenzocampo/device-endpoint@sha256:99212a0673ee9913d9c9e8f82c5dbb994f2bd54869ae0c1f3b3866ae93af52f0'

endpoint_rulesdata = [
    """
    On new fleet create secret
    """,
    {
        rulename: "on-new-fleet-create-service",
        subscribe_to: ["django.orm.post_save"],
        ruledata: {
            filters: [
                Filter(
                    lambda payload:
                    payload.get("signal_kwargs", {}).get("created", False)
                )
            ],
            processing: [
                SetSecretName("secret_name"),
                SetClusterLocalLabel("lbl_cluster_local"),
                Route("ensure-secret"),
                # fetch broker address
                K8sObjectsQuery(
                    apiversion="eventing.knative.dev/v1",
                    kind="Broker",
                    returns=lambda payload: lambda objs: (
                        payload.setdefault("k_sink", objs.get(name="data-received").obj["status"]["address"]["url"])
                    )
                ),
                K8sObjectCreate(lambda payload: {
                    "apiVersion": "serving.knative.dev/v1",
                    "kind": "Service",
                    "metadata": {
                        "labels": {**{"demo.krules.airspot.dev/app": "fleet-endpoint"}, **payload.get("lbl_cluster_local")},
                        "name": payload["data"]["name"],
                    },
                    "spec": {
                        "template": {
                            "metadata": {
                                "name": payload["secret_name"]
                            },
                            "spec": {
                                "containers": [{
                                    "image": IMAGE_DIGEST,
                                    "env": [
                                        {
                                            "name": "K_SINK",
                                            "value": payload["k_sink"],
                                        },
                                        {
                                            "name": "API_KEY",
                                            "valueFrom": {
                                                "secretKeyRef": {
                                                    "name": payload["secret_name"],
                                                    "key": "api_key"
                                                }
                                            }
                                        }
                                    ]
                                }]
                            }
                        }
                    }

                })
            ]
        }
    },
    """
    On fleet update (manage api_key and cluster-local)
    """,
    {
        rulename: "on-update-fleet-update-service",
        subscribe_to: ["django.orm.post_save"],
        ruledata: {
            filters: [
                Filter(
                    lambda payload:
                    not payload.get("signal_kwargs", {}).get("created", False)
                )
            ],
            processing: [
                SetSecretName("secret_name"),
                SetClusterLocalLabel("lbl_cluster_local"),
                Route("ensure-secret"),
                UpdateService(
                    secret_name=lambda payload: payload.get("secret_name"),
                    lbl_cluster_local=lambda payload: payload.get("lbl_cluster_local")
                )
            ],
        }
    },
]

secret_rulesdata = [
    """
    Responds to "ensure-secret", If secret already exists do nothing
    Create it otherwise
    Remove all others
    """,
    {
        rulename: "ensure-ingestion-apikey-secret",
        subscribe_to: "ensure-secret",
        ruledata: {
            filters: [
                K8sObjectsQuery(
                    apiversion="v1",
                    kind="Secret",
                    returns=lambda payload: lambda qobjs: (
                        qobjs.get_or_none(name=payload.get("secret_name")) is None
                    )
                )
            ],
            processing: [
                K8sObjectCreate(lambda payload: {
                    "apiVersion": "v1",
                    "kind": "Secret",
                    "type": "Opaque",
                    "metadata": {
                        "name": payload["secret_name"],
                        "labels": {
                            "app.krules.airspot.dev/owned-by": payload["data"]["name"]
                        }
                    },
                    "data": {
                        "api_key": base64.b64encode(payload["data"]["api_key"].encode("utf-8")).decode("utf-8")
                    }
                }),
                CleanUpSecrets(
                    owned_by=lambda payload: payload["data"]["name"],
                    other_than=lambda payload: payload["secret_name"],
                ),
            ]
        }
    }
]

rulesdata = endpoint_rulesdata + secret_rulesdata
