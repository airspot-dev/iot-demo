
from krules_core.base_functions import *

class PrepareSlackMessage(RuleFunctionBase):

    def execute(self):

        self.payload['url'] = self.configs["slack"]["webhooks"]["middleware_channel"]

        public = self.payload["value"].startswith("https")
        if public:
            self.payload["text"] = ":unlock: new *{}* available *publicly* for *{}* at {}".format(
                self.payload["subject_match"]["app"],
                self.payload["subject_match"]["fleet"],
                self.payload["value"]
            )
        else:
            self.payload["text"] = ":closed_lock_with_key: new *{}* available  *privately* for *{}* at {}".format(
                                        self.payload["subject_match"]["app"],
                                        self.payload["subject_match"]["fleet"],
                                        self.payload["value"]
            )

