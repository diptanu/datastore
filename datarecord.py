import utils

from documents import DataRecordDocument
from backend import DataBaseBackend
from uuid import uuid4

class DataRecord(object):

    def __init__(self, for_entity_uuid, record_dict, reported_at, uuid = None, voided = False):
        utils.setattributes(self, {'for_entity_uuid': for_entity_uuid,
                                   'reported_at': reported_at,
                                   'data': record_dict,
                                   'uuid': uuid,
                                   'voided': voided})

    def save(self):
        self.uuid = id = self.uuid if self.uuid is not None else  uuid4().hex
        document = DataRecordDocument(for_entity_uuid = self.for_entity_uuid,
                                      reported_at = self.reported_at, 
                                      data = self.data, id = id,
                                      voided = self.voided)
        
        return DataBaseBackend().save(document, self)

    def update(self):
        document = DataBaseBackend().get(self.uuid, DataRecordDocument())
        self._updateattr(document)
        DataBaseBackend().save(document, self)
        return self

    def invalidate(self):
        self.voided = True
        return self.update()

    def _updateattr(self, document):
        document.voided = self.voided
        document.data = self.data
