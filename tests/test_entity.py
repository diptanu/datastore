from datastore.entity import Entity
from datastore.entities import query
import unittest
import datetime

class TestEntity(unittest.TestCase):
    
    def test_create_entity(self):
        entity = Entity(geocode = "1234", geoname = "Ghana", unique_name = "Navio CHPS")
        entity.save()
        self.assertEqual(entity.geoname,'Ghana')
        
    def test_load_entity(self):
        entity = Entity(geocode = "123466", geoname = "Ghana", unique_name = "Navio CHPS")
        entity.save()
        
        loaded_entity = query.get(uuid=entity.uuid)
        self.assertEqual(loaded_entity.uuid, entity.uuid)
        
        
    def test_enity_has_created_at(self):
        entity = Entity(geocode = "1234", geoname = "Accra", unique_name = "Kajelo CHPS")
        entity.save()
        #FIXME Need Py2.7 to run the below code.
        #self.assertIfNotNone(entity.created_at)

    def test_add_data_record_to_entity(self):
        entity = Entity(geocode = "1234", geoname = "Accra", unique_name = "Kajelo CHPS")
        entity.save()

        data_record = entity.submit_datarecord(record_dict = {'name':'arv', 'value': '40', 'type':'int'}, reported_at = datetime.datetime.now())
        data_record.save()
        self.assertEqual(data_record.for_entity_uuid, entity.uuid)

    def test_if_reported_at_attribute_is_created(self):
        entity = Entity(geocode = "1234", geoname = "Accra", unique_name = "Kajelo CHPS")
        entity.save()

        data_record = entity.submit_datarecord(record_dict = {'name':'arv', 'value': '40', 'type':'int'}, reported_at = datetime.datetime.now())
        data_record.save()
        self.assertEqual(data_record.reported_at.date(), datetime.datetime.now().date())
        
    def test_single_aggregation_trees(self):
        aggregation_tree = {"org_chart": ["CEO", "Architect", "Developer"]}
        entity = Entity(geocode = "1234", geoname = "Accra", unique_name = "Kajelo CHPS", aggregation_tree = aggregation_tree)
        entity.save()
        
        loaded_entity = query.get(uuid=entity.uuid)
        self.assertEqual(loaded_entity.aggregation_tree['org_chart'], ["CEO", "Architect", "Developer"])

    def test_discover_data_types_of_the_datarecords(self):
        entity = Entity(geocode = "1234", geoname = "Gulu", unique_name = "Ashianti CHPS")
        entity.save()
        
        data_record = entity.submit_datarecord(record_dict = {'name':'arv', 'value': '12', 'type':'int'}, reported_at = datetime.date(2011,03,01))
        data_record.save()
        data_record = entity.submit_datarecord(record_dict = {'name':'patients', 'value': '1', 'type':'int'}, reported_at = datetime.date(2011,03,03))
        data_record.save()
        
        data_types = entity.get_data_records_types()
        self.assertEqual(data_types, {'patients': "int", 'arv': "int"})
        

    def test_entity_state(self):
        entity = Entity(geocode = "9876", geoname = "Gulu", unique_name = "Ashianti")
        entity.save()
        
        data_record = entity.submit_datarecord(record_dict = {'name':'arv', 'value': '12', 'type':'int'}, reported_at = datetime.date(2011,03,01))
        data_record = entity.submit_datarecord(record_dict = {'name':'arv', 'value': '1', 'type':'int'}, reported_at = datetime.date(2011,03,13))
        data_record.save()
        data_record = entity.submit_datarecord(record_dict = {'name':'patients', 'value': '1', 'type':'int'}, reported_at = datetime.date(2011,03,03))
        data_record.save()
        data_record = entity.submit_datarecord(record_dict = {'name':'patients', 'value': '15', 'type':'int'}, reported_at = datetime.date(2011,03,14))
        data_record.save()
        
        entity_state = entity.state({'arv':'latest', 'patients':'sum'})
        self.assertEqual(entity_state, {'patients':16, 'arv':1})
        
