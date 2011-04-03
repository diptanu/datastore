#Map
def map_fun(doc):
    if 'for_entity_uuid' in doc.keys():
        yield doc['for_entity_uuid'], doc['data']



#Sum
def sum_fun(keys, values, rereduce):
    aggregated_result = {}
    for value in values:
        data_type, name, val = value['type'], value['name'], value['value']
        if data_type == 'int':
            if name in aggregated_result.keys():
                aggregated_result[name] = int(aggregated_result[name]) + int(val)
            else:
                aggregated_result[name] = val

    return aggregated_result


#Latest
def fun(keys, values, rereduce):
    aggregated_result = {}
    for value in values:
        name, val = value['name'], value['value']
        aggregated_result[name] = val
        
    return aggregated_result


#Get All data attributes of Entity
def fun(keys, values, rereduce):
    aggregated_result = {}
    for value in values:
        name, data_type = value['name'], value['type']
        aggregated_result[name] = data_type

    return aggregated_result

#Map Function
'''
function(doc){
if(doc.for_entity_uuid && !doc.voided){
emit([doc.for_entity_uuid, Date.parse(doc.reported_at)], doc.data);
}
}
'''

#Sum
'''
function(keys, values){
   aggregated_result = {};
   for(i in values){
      type = values[i].type;
      name = values[i].name;
      val = values[i].value;
      if(type == "int"){
          if(aggregated_result[name] == undefined){
             aggregated_result[name] = parseInt(val);
          }else{
             aggregated_result[name] = aggregated_result[name] + parseInt(val);
          }
      }

   }
return aggregated_result;
}
'''

#DataTypes
'''
function(keys, values){
aggregated_result = {};
for(i in values){
name = values[i].name;
type = values[i].type;
aggregated_result[name] = type;
}
return aggregated_result;
}
'''

#Latest
'''
function(keys, values){
aggregated_result = {};
for(i = values.length -1; i >= 0; i-- ){
name = values[i].name;
val = values[i].value;
aggregated_result[name] = parseInt(val);
}
return aggregated_result;
}
'''
