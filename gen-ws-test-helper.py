from jinja2 import Environment, FileSystemLoader
from random import *
import os
import uuid



def generate_test_helper():
    with open('test-class.txt', 'r') as input_file:
        abstract = input_file.readline().strip() == 'A'
        test_class, test_super_class = two(input_file.readline().strip().split())
        result_class = input_file.readline().strip()
        attributes = [line.strip().split(' : ') for line in input_file]
    print(test_class, test_super_class)
    print(result_class)
    print(attributes)
    test_class_inc_dir = get_inc_dir(test_class)
    result_class_inc_dir = get_inc_dir(result_class)
    helper_class_name = 'Helper' + test_class[2:] if test_class.startswith('Pv') else test_class
    helper_class_name_ext = ''
    call_super_init = False
    if abstract:
        helper_class_name = 'Abstract' + helper_class_name
        helper_class_name_ext = '<T extends ' + test_class + ', R extends ' + result_class + '>'
    if test_super_class is None:
        if abstract:
            helper_super_class_name = 'Helper<T, R>'
        else:
            helper_super_class_name = 'Helper<' + test_class + ', ' + result_class + '>'
    else:
        call_super_init = True
        tmp = test_super_class[2:] if test_super_class.startswith('Pv') else test_super_class
        if abstract:
            helper_super_class_name = 'AbstractHelper' + tmp + '<T, R>'
        else:
            helper_super_class_name = 'AbstractHelper' + tmp + '<' + test_class + ', ' + result_class + '>'

    java_test_class_file = open(helper_class_name + '.java', 'w')
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    java_test_class_file.write(j2_env.get_template('helper.tmpl').render(
            helper_class_name=helper_class_name + helper_class_name_ext,
            helper_super_class_name=helper_super_class_name,
            test_class=test_class,
            test_super_class=test_super_class,
            result_class=result_class,
            attributes=attributes,
            test_class_inc_dir=test_class_inc_dir,
            result_class_inc_dir=result_class_inc_dir,
            get_attr_type=get_type,
            get_attr_value=get_value,
            call_super_init=call_super_init,
            create_test_object=not abstract
    ))
    java_test_class_file.close()

def two(elements):
    if len(elements) == 1:
        return [elements[0], None]
    else:
        return elements

def get_type(type):
    switcher = {
        'boolean': 'Boolean',
        'short': 'Short',
        'int': 'Integer',
        'long': 'Long'
    }
    return switcher.get(type, type)

def get_value(type):
    if type == 'PvEJaNeinUnbekannt':
        return 'PvEJaNeinUnbekannt.JA' if randint(0,1) == 1 else 'PvEJaNeinUnbekannt.NEIN' if randint(0,1) == 1 else 'PvEJaNeinUnbekannt.UNBEKANNT'
    if type.startswith("PvE"):
        return type + '.'

    switcher = {
        'String': '"' + str(uuid.uuid4())[:8] + '"',
        'Boolean': 'Boolean.TRUE' if randint(0,1) == 1 else 'Boolean.FALSE',
        'Short': '(short) ' + str(randint(1, 1000)),
        'Long': str(randint(1, 1000)) + 'L',
        'Integer': str(randint(1, 1000)),
        'Double': str(randint(1, 1000)) + '.' + str(randint(1, 99)) + 'd',
        'Date': 'new Date()',
        'BigDecimal': 'new BigDecimal(' + str(randint(1, 10000)) +'.' + str(randint(1, 99)) + ')',
        'Timestamp': 'Timestamp.valueOf(LocalDateTime.now())',
        'PvTDatum': 'PvTDatum.fromISO("{}-{:02d}-{:02d}")'.format(randint(1980, 2020), randint(1,12), randint(1,28)),
        'PvTBetrag': 'new PvTBetrag("{},{} EUR")'.format(randint(500, 9999), randint(10,99)),
        'PvTWaehrung': 'PvTWaehrung.euro()',
        'PvTProzentsatz': 'new PvTProzentsatz(BigDecimal.valueOf({}.{}))'.format(randint(0,99), randint(0,99))
    }
    xtype = type[2:] if type.startswith('Pv') else type
    return switcher.get(type, 'new Helper' + xtype + '()')


def get_inc_dir(class_name):
    if class_name.startswith("PvT"):
        return 'de.provinzial.leistung.common'
    elif class_name.lower().find('eingabe') != -1:
        return 'de.provinzial.leistung.webservice.v1.eingabe'
    elif class_name.lower().find('rueckgabe') != -1:
        return 'de.provinzial.leistung.webservice.v1.rueckgabe'
    return 'de.provinzial.leistung.webservice.v1.beans'


THIS_DIR =  os.path.dirname(os.path.abspath(__file__))
print(THIS_DIR)

ATTR_TEST_VAL_TMPL='''
public static final TVal<{{type}}> {{name}} = create("{{label}}", {{value}});
'''

if __name__ == '__main__':
    generate_test_helper()
