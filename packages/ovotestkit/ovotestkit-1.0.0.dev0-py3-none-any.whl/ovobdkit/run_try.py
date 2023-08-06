from ovodevkit import utils
from ovodevkit.utils import FieldDefinition, FieldList

def test_field_definition():
    schema = '''
        field0 unsigned int
        field1 string
        field2 Decimal( 30, 8)
        field3  Float
        date_partition String	*
    '''
    fields, partitions = utils.parse_schema(schema)
    print("fields : ",fields)
    print("partitions : ",partitions)

def test_dict():
    fdef = FieldDefinition()
    fdef['field1'] = 'string'
    fdef['field2'] = 'int'
    fdef['field3'] = 'string'
    
    assert str(fdef) == 'field1 string, field2 int, field3 string'

def test_list():
    fdef = FieldList()
    fdef.append('field1')
    fdef.append('field2')
    fdef.append('field3')
    assert str(fdef) == 'field1, field2, field3'

def test_field_conversion():
    src_schema = '''
        field0 unsigned int
        field1 string
        field2 Decimal( 30, 8)
        field3  Float
        date_partition String	*
    '''

    tgt_schema = '''
        id bigint
        name string
        value Decimal( 30, 8)
        average  Float
        date_partition String	*
    '''


    s_fields, s_partitions = utils.parse_schema(src_schema)
    t_fields, t_partitions = utils.parse_schema(tgt_schema)

    converted = utils.convert_fields(s_fields + s_partitions, t_fields + t_partitions)
    print(converted)


# print_string()    
# test_list()
# test_field_definition()
test_field_conversion()

# main()