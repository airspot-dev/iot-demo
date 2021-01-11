
name = "on-temp-status-change-notifier-slack"

add_files = (
    "ruleset.py",
)

add_modules = True  # find modules in directory (folders having __init__.py file) and add them to container

extra_commands = (
#    ("RUN", "pip install my-wonderful-lib==1.0")
)

labels = {
    "serving.knative.dev/visibility": "cluster-local",
    "krules.airspot.dev/type": "ruleset",
    "krules.airspot.dev/ruleset": name,
    "configs.krules.airspot.dev/slack-webhooks": "inject"
}

template_annotations = {
    #"autoscaling.knative.dev/minScale": "0",
}

#service_account = "my-service-account"

triggers = (
   {
       "name": "on-temp-status-change-notifier-slack-back-to-normal",
       "filter": {
           "attributes": {
               "type": "temp-status-back-to-normal"
           }
       }
   },
   {
       "name": "on-temp-status-change-notifier-slack-status-bad",
       "filter": {
           "attributes": {
               "type": "temp-status-bad"
           }
       }
   },
   {
       "name": "on-temp-status-change-notifier-slack-status-still-bad",
       "filter": {
           "attributes": {
               "type": "temp-status-still-bad"
           }
       }
   },
)
triggers_default_broker = "class-a"

ksvc_sink = "broker:default"
ksvc_procevents_sink = "broker:procevents"

