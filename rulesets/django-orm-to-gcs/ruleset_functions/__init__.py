from cloudstorage.drivers.google import GoogleStorageDriver
from krules_core.base_functions import RuleFunctionBase


class CreateFleetGCSFolder(RuleFunctionBase):
    def execute(self, bucket, fleet):
        driver = GoogleStorageDriver()
        bucket = driver.get_container(bucket)
        bucket.upload_blob("%s/import/class-a/" % fleet)
        bucket.upload_blob("%s/import/class-b/" % fleet)
