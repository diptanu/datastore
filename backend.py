import datetime
from time import mktime

from couchdb.http import ResourceNotFound
from couchdb import Server
from couchdb.mapping import DateTimeField

DATABASE_NAME = 'mangrove'
SERVER_HOST = 'http://0.0.0.0:5984'
DESIGN_DOCUMENT_NAME = 'aggregation'
VIEWS = {'latest': 'latest', 'data_types': 'data_types', 'sum':'sum'}

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
        view_url = '_design/'+ DESIGN_DOCUMENT_NAME +'/_view/' + VIEWS['data_types']
        rows = self.database.view(view_url, group=True, group_level = 1).rows
        return self.filter_rows_by_uuid(entity.uuid, rows)

    def get_data_records_aggregated(self, entity, data_records_func, asof):
        aggregated_result = {}
        endkey = [entity.uuid, int(mktime(asof.timetuple())) * 1000]
        for name, aggregation_type in data_records_func.items():
            view_url = '_design/' + DESIGN_DOCUMENT_NAME + '/_view/' + VIEWS[aggregation_type]
            rows = self.database.view(view_url, group=True, group_level = 1, endkey = endkey).rows
            data = self.filter_rows_by_uuid(entity.uuid, rows)
            aggregated_result[name] = data[name] if name in data.keys() else None
            
        return aggregated_result

    def filter_rows_by_uuid(self, uuid, rows):
        value = None
        for row in rows:
            if row.key[0] == uuid:
                value = row.value
                break
        
        return value
        

    def get(self, uuid, document):
        return document.load(self.database, uuid)
        
    def __unicode__(self):
        return u"Connected on %s - working on %s" % (self.url, self.database_name)

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return repr(self.database)
