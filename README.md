# IoT demo application

The aim of this demo is to highlights some KRules' core concepts such as the subjects' **reactive properties**, 
which are used not just to map a digital twin of the devices and giving them a state to which changes we can 
react. This may be expected in an IoT scenario. In the same way we react to devices produced metrics such 
as a temperature sensor value, we also react to Kubernetes resources update events, gathering pieces of 
information we are interested in and setting them as reactive properties of a _subject_ representing, in 
that case, the twin of the resource.
This is the case of a newly created Knative service for which we want to listen and react when a URL becomes 
available or changes following the provisioning of the SSL cert. This is made very easily

The Demo also wants to focus on how easy it is to take full advantage of Knative eventing, using brokers 
and triggers and shape logic upon them using subjects' **extended properties** so that any time we produced a 
_CloudEvent_ related to a specific device (the subject) its metadata automatically contains those properties 
determining the activation or not of o specific groups of rulesets

Demo starts form uploading a .csv file, containing the base information about a set of devices, on a 
Google Cloud Storage bucket. 
This is bound by a Knative CloudStorageSource, a ruleset subscribe to the produced CloudEvents. 
A device subject is created for each line of csv file and, depending in which folder the file was uploaded, 
an _extended property_ is set defining an hypothetical "class of device" conditioning all subsequent events 
related to the device allowing triggers to act differently.
In particular, telemetry data are routed on a common broker but they are also split in two different brokers 
specific for class of devices having as a result to activate a common set of logic for all devices 
(eg: monitoring the _receiving data_ state) and specific logic for each class of device simply subscribing 
to appropriate broker.
In particular, for one class we are interested in logic related to temperature sensor value and for the 
other we are tracking geo positioning.

For ingestion we simply use an http endpoint provided by a serverless Knative service.
The service (and its related secret containing and the api key) is initially created starting from a 
database model created in a simple Django application for which an ad-hoc extension produces cloudevents 
for any create/update/delete operation on Django ORM for models we are interested in. Each update 
operation originates a new Knative service revision. This, in fact, make the Django application 
acting as another Knative source.

For more detailed information about how the demo works you can take a look to these [slide](https://github.com/airspot-dev/iot-demo/blob/master/Diagrams.pdf)

Note that a step-by-step installation guide for this demo doesn't exist yet, but, if you are interested 
in knowing more about the project or even contribute to it don't esitate to [contact us](mailto:info@airspot.tech)