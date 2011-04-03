from datastore.entity import Entity, DataRecord
from datastore.backend import DataBaseBackend
from datastore.documents import EntityDocument, DataRecordDocument

def get(uuid):
    document = DataBaseBackend().get(uuid, EntityDocument())
    entity = Entity(geocode = document.geocode, geoname = document.geoname, unique_name = document.unique_name, aggregation_tree = document.aggregation_tree, uuid = document.id)
    return entity

def get_data_record(uuid):
    document = DataBaseBackend().get(uuid, DataRecordDocument())
    datarecord = DataRecord(for_entity_uuid = document.for_entity_uuid, record_dict = document.data, reported_at = document.reported_at, uuid = document.id, voided = document.voided)
    return datarecord
    
def entities_for_ids(uids):
    ''' return list of entities for given uids '''
    entities = []
    for uid in uids:
        try:
            entities.append(get(uid))
        except:
            # guess there wasn't an entity with that id
            pass

        return entities

def entities_for_attributes(attrs):
    '''
    retrieve entities with datarecords with the given
    named attributes. Can be used to search for entities
    by identifying info like a phone number
    
    Include 'type' as an attr to restrict to a given entity type
    
    returns a sequence of 0, 1 or more matches
    
    ex:
    attrs = { 'type':'clinic', 'name': 'HIV Clinic' }
    print entities_for_attributes(attrs)
    
    '''
    
    pass

# geo aggregation specific calls
def entities_near(geocode, radius=1, attrs=None):
    '''
    Retrieve an entity within the given radius (in kilometers) of
    the given geocode that matches the given attrs
    
    Include 'type' as an attr to restrict to a given entity type
    
    returns a sequence
    
    '''
    pass

def entities_in(geoname, attrs=None):
    '''
    Retrieve an entity within the given fully-qualified geographic
    placename.
    
    Include 'type' as an attr to restrict to a given entity type
    
    returns a sequence
    
    ex.
    found = entities_in(
    [us,ca,sanfrancisco],
    {'type':'patient', 'phone':'4155551212'}
    )
    
    '''
    pass
