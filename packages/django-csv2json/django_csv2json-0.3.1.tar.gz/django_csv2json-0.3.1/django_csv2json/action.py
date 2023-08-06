import ujson as json
import csv
from django.utils.text import slugify
from django_csv2json.funciones import read_file, add_list
import os
from pathlib import Path

class CSV2JSON:
    """
    models :: a dict, every key is a model, the value is a set of the field-names
    file :: the csv file
    field :: the field that has a slug on the django model
    opts :: the fields that need to transform (str->int, str->bool)
    switch :: a dict, with the field names changed from csv to django model    
    """
    fields = ["models", "file", "field", "opts", "switch"]
    def __init__(self,
                 *args,
                 **kwargs):
        self.origin = Path(kwargs.get('origin', './csv').strip().rstrip("/").strip())
        self.destiny = Path(kwargs.get('destiny', './json').strip().rstrip("/").strip())
        if not self.destiny.exists():
            os.makedirs(str(self.destiny))
        self.files = kwargs.get('files',
                                (None, None, None, {}))
        for file_elem in self.files:
            models, file_name, field, condition, switch = tuple(map(file_elem.get, self.fields))
            data_dict = self.read_file(
                models,
                file_name,
                field,
                condition,
                switch
            )
            for model in models:
                data_list = data_dict.get(model)
                if data_list:
                    self.write_json(model, data_list)

    def read_file(self,
                  models: dict = {},
                  file_name: str = "",
                  field: str = "",
                  condition: dict = {},
                  switch: dict = {}):
        path = self.origin/file_name
        data_dict = {model:[] for model in models.keys()}
        if path.exists():
            print("Reading...", path)
            field_slug = "slug_%s" % field
            with open(path, 'r') as read:
                reader = csv.DictReader(read, delimiter=';')
                for row in reader:
                    for model, keys in models.items():
                        dict_data = {}
                        for key, value in row.items():
                            if not key == "id" and key.lower() in keys:
                                if condition.get(key):
                                    value = condition.get(key)(value)
                                elif value:
                                    value = value.strip()
                                else:
                                    value = ""
                                key = switch.get(key, key)
                                dict_data.update({key.lower(): value})
                        if field:
                            main_field = row.get(field)
                            dict_data.update({field_slug: slugify(main_field)})
                        new_data = {
                            "model": model,
                            "pk": int(row.get('id', "0 ").strip()),
                            "fields": dict_data}
                        data_dict[model].append(new_data)
        return data_dict

    def write_json(self, file_name, data_list):
        new_file_path = "%s/%s.json" % (
            self.destiny, file_name)
        print("Saving json...", new_file_path)
        with open(new_file_path, 'w') as write_json:
            write_json.write("[\n")
            len_list = len(data_list)
            for i, elem in enumerate(data_list):
                json.dump(elem, write_json, indent=2)
                if i < len_list-1:
                    write_json.write(',\n')
                else:
                    write_json.write('\n')
            write_json.write("]")
