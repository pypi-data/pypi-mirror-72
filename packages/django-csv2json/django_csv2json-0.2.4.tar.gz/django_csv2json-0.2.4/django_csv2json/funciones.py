def read_file(file_path):
    with open(file_path, 'r') as reader:
        archivo = reader.readlines().pop()
        return archivo


def add_list(elem_list):
    """
    Para referenciar a elementos de otros modelos
    """
    lista = []
    lista.append(elem_list)
    return lista


def field2list(field, separator='|'):
    return field.split(separator)


def many2many_dict(names, field, separator='|'):
    return dict(zip(names, field2list(field, separator)))


def many2many_list(field, separator_1="|", separator_2='#'):
    return [field2list(field_e, separator_2) for field_e in field2list(field)]
