from django_csv2json.action import CSV2JSON
from django_csv2json.funciones import read_file, add_list
import click
from pathlib import Path

@click.command()
@click.option("--origen",
              default="./csv",
              show_default=True, help="Ruta al directorio que contiene archivos csv")
@click.option("--destino",
              default="./json",
              show_default=True, help="Ruta al directorio para almacenar json")
@click.option("--files_json",
              default="./files.json",
              show_default=True,
              help="Archihvo con las settings de archivos, con llaves {model, file, field, opts}")
def csv2json(origen, destino, files_json):
    files = []
    files_json_path = Path(files_json)
    if not files_json_path.exists():
        fields = ["models", "file", "field", "opts"]
        files = [
            dict(zip(fields,
                     ({
                         'station.station':{"name","code","ecef_x","ecef_y","ecef_z"},
                         "station.inetdata":{"name","interface_host","interface_port",
                                             "protocol_host", "protocol_port", "protocol",
                                             "network_id"}
                     }, 'station.csv', 'name',
                      {"port":int, "interface_port":int, "active":bool}, {}))),
            dict(zip(fields,
                     ({'database.dbdata':{"name","path","host","port","user","passw", "info", "dbtype"}},
                      'dbdata_info.csv',
                      'name', {"port": int}, {}))),
            dict(zip(fields,
                     ({'database.dbtype':{"typedb","name","url","data_list"}},
                      'dbtype.csv',
                      'name', {}, {}))),
            dict(zip(fields,
                     ({"network_register.network_register":{"name","url","description"}}, "network.csv",
                      "name", {}, {}))),
            dict(zip(fields,({"server.server":{"host_name","host_ip","gnsocket_port","activated"}},
                             "server.csv",
                             "host_name", {"gnsocket_port":int, "activated":bool}, {}))),
        ]
    else:
        print("Leyendo de ./files.json")
        with open(files_json_path) as fj:
            files = json.loads(fj)
    opts = {
        "origen":origen,
        "destino":destino,
        "files":files
    }
    CSV2JSON(**opts)


