import datetime

from couchdb.mapping import Document, TextField, DictField, DateTimeField, ListField, Mapping, ViewField

class EntityDocument(Document):
    
    geoname = TextField()
    geocode = TextField()
    unique_name= TextField()
    aggregation_tree = DictField()
    created_at = DateTimeField(default = datetime.datetime.now())


from mapreduce import map_fun, sum_fun
class DataRecordDocument(Document):
    
    for_entity_uuid = TextField()
    data = DictField(Mapping.build(
            name = TextField(),
            value = TextField(),
            type = TextField()))
    reported_at = DateTimeField()
    created_at = DateTimeField(default = datetime.datetime.now())
    by_sum = ViewField('general', map_fun, sum_fun, name="test_sum", language="python")



