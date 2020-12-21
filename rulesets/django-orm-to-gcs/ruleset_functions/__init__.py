from google.cloud import storage
from krules_core.base_functions import RuleFunctionBase


def create_gcs_folder(bucket, name):
    blob = bucket.blob(name)
    blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')


class CreateFleetGCSFolders(RuleFunctionBase):

    def execute(self, bucket, fleet):
        client = storage.Client()
        bucket = client.get_bucket(bucket)
        create_gcs_folder(bucket, "%s/import/class-a/" % fleet)
        create_gcs_folder(bucket, "%s/import/class-b/" % fleet)
