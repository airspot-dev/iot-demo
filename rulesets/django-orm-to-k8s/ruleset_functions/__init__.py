from app_functions import hashed
from k8s_functions import K8sObjectsQuery
from krules_core.base_functions import SetPayloadProperty


class SetSecretName(SetPayloadProperty):

    def execute(self, payload_target, **kwargs):

        name = hashed(
            self.payload["data"]["name"],
            self.payload["data"]["api_key"], self.payload["data"]["name"]
        )
        super().execute(payload_target, name)


class SetClusterLocalLabel(SetPayloadProperty):

    def execute(self, payload_target, **kwargs):

        super().execute(
            payload_target, eval(self.payload.get("data").get("cluster_local")) and {
                        "serving.knative.dev/visibility": "cluster-local"
                } or {}
        )


class CleanUpSecrets(K8sObjectsQuery):

    def execute(self, **kwargs):

        owned_by = kwargs.get("owned_by", self.payload["data"]["name"])
        other_than = kwargs.get("other_than", self.payload["secret_name"])

        to_delete = []

        super().execute(
            apiversion="v1",
            kind="Secret",
            selector={
                "app.krules.airspot.dev/owned-by": owned_by,
            },
            foreach=lambda obj: (
                obj.name != other_than and to_delete.append(obj)
            )
        )

        for obj in to_delete:
            obj.delete()


class UpdateService(K8sObjectsQuery):

    def _update_obj(self, obj, secret_name, lbl_cluster_local):
        obj.obj["spec"]["template"]["metadata"]["name"] = secret_name
        if "serving.knative.dev/visibility" in obj.obj["metadata"]["labels"]:
            del obj.obj["metadata"]["labels"]["serving.knative.dev/visibility"]
        obj.obj["metadata"]["labels"].update(lbl_cluster_local)
        for container in obj.obj["spec"]["template"]["spec"]["containers"]:
            if container["name"] == "user-container":
                for env in container["env"]:
                    if env["name"] == "API_KEY":
                            env["valueFrom"]["secretKeyRef"]["name"] = secret_name

        self.payload["_updated_object"] = obj.obj
        obj.update()

    def execute(self, **kwargs):

        secret_name = kwargs.get("secret_name", self.payload.get("secret_name"))
        lbl_cluster_local = kwargs.get("lbl_cluster_local", self.payload.get("lbl_cluster_local"))

        super().execute(
            apiversion="serving.knative.dev/v1", kind="Service",
            selector={
                "demo.krules.airspot.dev/app": "fleet-endpoint"
            },
            returns=lambda qobjs: (
                self._update_obj(qobjs.get_by_name(self.payload.get("data").get("name")), secret_name, lbl_cluster_local)
            )
        )
