from app_functions import hashed
from krules_core.base_functions import SetPayloadProperty


class SetSecretName(SetPayloadProperty):

    def execute(self, payload_target, **kwargs):

        name = hashed(
            self.payload["data"]["name"],
            self.payload["data"]["api_key"], self.payload["data"]["name"]
        )
        super().execute(payload_target, name)