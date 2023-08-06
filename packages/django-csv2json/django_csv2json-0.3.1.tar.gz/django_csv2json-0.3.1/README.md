Repository
============

Download the module from:

http://gitlab.csn.uchile.cl/dpineda/csv2json

CSV to JSON
============

This module is a conversor from csv data to json.

The main goal is create a json file for *Django models*.

The *csv* must have the same fields as the *django model*

The *fields related* to *another models* uses the *natural key*. So every model must have a *natural_key* method.

The third argument


How to Install
=================

Using *pip*

```bash
pip install django_csv2json
```

From the repository

```bash
python setup.py install
```

How to use
===========

This modules dispose a class *CSV2JSON*, that requires a origin folder, a destiniy folder and a list of files. Every element from this list must be a *dictionary* with the keys "{model, file, field, opts}".

Also, there are a command to use on the *command line*.

```bash
csv2json --origin "./csn" --destiny "./json" --file_json "./files.json"
```

For help, type

```bash
csv2json --help
```

Campos de files.json
========================

Debe contener un campo *models* con los modelos de *Django* que contengan campos en el *csv*, determinar sus llaves.

Debe contener el archivo *file* csv.

Debe contener el *field* del cual se transforma un *slug* (un string formateado a sencillo)

Debe contener un dciccionario con las opciones o formato específico a cada campo.

Debe incluirse un diccionario (vacío) o que contenga el cambio en el nombre de los campos de csv al modelo django.


```python
    fields = ["models", "file", "field", "opts", "switch"]

    files = [
        dict(zip(fields,({'organization.kindoforganization':{"logo","name","acronim", "url"}},
         'kindoforganization.csv', 'name',
         {"description": read_file}, {}))),
        dict(zip(fields,({'organization.organizationinfo':{"name","description","url_wiki"}},
         'organization.csv',
         'name', {"kind": add_list}, {}))),
    ]
    kwargs = {
        'files': files,
        'origin': './csv',
        'destiny': './json'
    }
    CSV2JSON(**kwargs)

```





