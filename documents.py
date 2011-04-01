import datetime

from couchdb.mapping import Document, TextField, DictField, DateTimeField, ListField

class EntityDocument(Document):
    
    geoname = TextField()
    geocode = TextField()
    unique_name= TextField()
    aggregation_tree = DictField()
    created_at = DateTimeField(default = datetime.datetime.now())


class DataRecordDocument(Document):
    
    for_entity_id = TextField()
    data = DictField()
    reported_at = DateTimeField()
    created_at = DateTimeField(default = datetime.datetime.now())

