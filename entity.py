#
# Entity class is main way of interacting with Entities AND datarecords.
# Datarecords are always submitted/retrieved from an Entity
#

import datetime

from backend import DataBaseBackend
from documents import EntityDocument, DataRecordDocument
from uuid import uuid4

class DataRecord(object):

    def __init__(self, for_entity_uuid, record_dict, reported_at, uuid = None):
        setattr(self, 'for_entity_uuid', for_entity_uuid)
        setattr(self, 'reported_at', reported_at)
        setattr(self, 'data', record_dict)
        setattr(self, 'uuid', uuid)

    def save(self):
        id = self.uuid = uuid4().hex
        document = DataRecordDocument(for_entity_uuid = self.for_entity_uuid, reported_at = self.reported_at, data = self.data)
        return DataBaseBackend().save(document, self)

class Entity(object):
    
    def __init__(self, geocode = None, geoname = None, unique_name = None, aggregation_tree = None, uuid = None):
        
        data = {'geocode': geocode, 'geoname':geoname, 'unique_name' : unique_name, 'aggregation_tree':aggregation_tree, 'uuid': uuid}
        for key, value in data.items():
            setattr(self, key, value)
                
    def save(self):
        id = self.uuid = uuid4().hex
        document = EntityDocument(id=id, geoname = self.geoname, unique_name = self.unique_name, aggregation_tree = self.aggregation_tree)
        return DataBaseBackend().save(document, self)
        
    def submit_datarecord(self, record_dict, created_at):
        data_record = DataRecord(self.uuid, record_dict, created_at)
        return data_record

        
    def update_datarecord(self,uid,record_dict):
        self.invalidate_datarecord(uid)
        return self.submit_datarecord(record_dict, datetime.datetime.now())

    def invalidate_datarecord(self,uid):
        pass

    def revalidate_datarecord(self,uid):
        pass


    def current_state(self):
        return self.state(None)

    def state(self, asof=None):
        pass
