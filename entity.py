import datetime

from backend import DataBaseBackend
from documents import EntityDocument, DataRecordDocument
from datarecord import DataRecord
from uuid import uuid4


class Entity(object):
    
    def __init__(self, geocode, geoname, unique_name, aggregation_tree = None, uuid = None):
        
        data = {'geocode': geocode, 'geoname':geoname, 'unique_name' : unique_name, 'aggregation_tree':aggregation_tree, 'uuid': uuid}
        for key, value in data.items():
            setattr(self, key, value)
                
    def save(self):
        self.uuid = id = self.uuid if self.uuid is not None else uuid4().hex
        document = EntityDocument(id=id,
                                  geoname = self.geoname, 
                                  geocode = self.geocode, 
                                  unique_name = self.unique_name, 
                                  aggregation_tree = self.aggregation_tree)
        return DataBaseBackend().save(document, self)
        
    def submit_datarecord(self, record_dict, reported_at):
        data_record = DataRecord(self.uuid, record_dict, reported_at)
        return data_record

        
    def update_datarecord(self,uid,record_dict):
        self.invalidate_datarecord(uid)
        return self.submit_datarecord(record_dict, datetime.datetime.now())

    def invalidate_datarecord(self, data_record):
        data_record.invalidate()

    def revalidate_datarecord(self,uid):
        pass

    def get_data_records_types(self):
        return DataBaseBackend().get_data_records_type(self)
    
    def current_state(self, data_records_func):
        return self.state(data_records_func)

    def state(self, data_records_func, asof = datetime.datetime.now()):
        '''
        for example data_records_func = {'arv':'latest', 'num_patients':'sum'}
        '''
        return DataBaseBackend().get_data_records_aggregated(self, data_records_func, asof)
