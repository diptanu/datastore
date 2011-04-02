import datetime

from couchdb.http import ResourceNotFound
from couchdb import Server
from couchdb.mapping import DateTimeField

DATABASE_NAME = 'mangrove'
SERVER_HOST = 'http://0.0.0.0:5984'

#FIXME: Duplicated it for the sake of the spike
class DataBaseBackend(object):

    def __init__(self, server=SERVER_HOST, database_name = DATABASE_NAME, *args, **kwargs):
        self.url = server
        self.server = Server(self.url)
        try:
            self.database = self.server[database_name]
        except ResourceNotFound:
            self.database = self.server.create(database_name)

    def save(self, document, obj):
        document.store(self.database)
        return obj

    def get_data_records_type(self, entity):
        rows = self.database.view('_design/aggregation1/_view/data_types1', group=True)
        value = None
        for row in rows:
            if row.key == entity.uuid:
                value = row.value
                break
            
        return value
        
    def get_data_records(self, entity, data_records_func, asof):
        return entity
    
    def get(self, uuid, document):
        return document.load(self.database, uuid)
        
    def __unicode__(self):
        return u"Connected on %s - working on %s" % (self.url, self.database_name)

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return repr(self.database)
