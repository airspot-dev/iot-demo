
name = "on-location-change-notifier-slack"

add_files = (
    "ruleset.py",
)

add_modules = True  # find modules in directory (folders having __init__.py file) and add them to container

extra_commands = (
#    ("RUN", "pip install my-wonderful-lib==1.0"),
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
       "name": name,
       "filter": {
           "attributes": {
               "type": "subject-property-changed",
               "propertyname": "location",
           }
       }
   },
)
triggers_default_broker = "class-b"

ksvc_sink = "broker:default"
ksvc_procevents_sink = "broker:procevents"

