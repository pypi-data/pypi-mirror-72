from django_csv2json.action import CSV2JSON
from django_csv2json.funciones import read_file, add_list
import click

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
        fields = ["model", "file", "field", "opts"]
        files = [
            dict(zip(fields,
                     ('station.station', 'station.csv', 'name', {}))),
            dict(zip(fields,
                     ('database.dbdata', 'dbdata_info.csv',
                      'name', {"port": int, "dbtype": add_list}))),
            dict(zip(fields,
                     ("network_register.network_register", "network.csv",
                      "name", {}))),
            dict(zip(fields,("server.server", "server.csv",
                             "host_name", {}))),
            dict(zip(fields,('database.dbtype', 'dbtype.csv',
                             'name', {})))
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


