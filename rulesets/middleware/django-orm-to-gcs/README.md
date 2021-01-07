# django-orm-to-gcs

responds to the events of creation / deletion of the "Fleet" model on the django orm,
creating or destroying the directories structure on gcs bucket

the generated structures are <fleet_name>/class-a/import and <fleet_name>/class-a/import