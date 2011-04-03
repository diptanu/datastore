import datetime

from couchdb.mapping import Document, TextField, DictField, DateTimeField, ListField, Mapping, BooleanField

class EntityDocument(Document):
    
    geoname = TextField()
    geocode = TextField()
    unique_name= TextField()
    aggregation_tree = DictField()
    created_at = DateTimeField(default = datetime.datetime.now())


class DataRecordDocument(Document):
    
    for_entity_uuid = TextField()
    data = DictField(Mapping.build(
            name = TextField(),
            value = TextField(),
            type = TextField()))
    reported_at = DateTimeField()
    voided = BooleanField(default = False)
    created_at = DateTimeField(default = datetime.datetime.now())



