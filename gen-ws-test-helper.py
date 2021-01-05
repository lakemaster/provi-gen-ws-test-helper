from jinja2 import Environment, FileSystemLoader
from random import *
import os
import uuid



def generate_test_helper():
    with open('test-class.txt', 'r') as input_file:
        test_class = input_file.readline().strip()
        result_class = input_file.readline().strip()
        attributes = [line.strip().split()[1:3] for line in input_file]
    #print(test_class)
    #print(result_class)
    #print(attributes)
    test_class_inc_dir = get_inc_dir(test_class)
    result_class_inc_dir = get_inc_dir(result_class)
    helper_class_name = 'Helper' + test_class[2:] if test_class.startswith('Pv') else test_class
    java_test_class_file = open(helper_class_name + '.java', 'w')
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    java_test_class_file.write(j2_env.get_template('helper.tmpl').render(
            helper_class_name=helper_class_name,
            test_class=test_class,
            result_class=result_class,
            attributes=attributes,
            test_class_inc_dir=test_class_inc_dir,
            result_class_inc_dir=result_class_inc_dir,
            get_attr_type=get_type,
            get_attr_value=get_value
    ))
    java_test_class_file.close()

def get_type(type):
    switcher = {
        'boolean': 'Boolean',
        'short': 'Short',
        'int': 'Integer',
        'long': 'Long'
    }
    return switcher.get(type, type)

def get_value(type):
    if type.startswith("PvE"):
        return type + '.'

    switcher = {
        'String': '"' + str(uuid.uuid4())[:8] + '"',
        'Boolean': 'Boolean.TRUE',
        'Short': '(short) ' + str(randint(1, 1000)),
        'Long': str(randint(1, 1000)) + 'L',
        'Integer': str(randint(1, 1000)),
        'Date': 'new Date()',
        'BigDecimal': 'new BigDecimal(' + str(randint(1, 10000)) +'.' + str(randint(1, 99)) + ')',
        'Timestamp': 'Timestamp.valueOf(LocalDateTime.now())'
    }
    return switcher.get(type, 'new Helper' + type + '()')


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
