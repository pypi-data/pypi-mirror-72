from setuptools import setup

setup(name='django_csv2json',
      version='0.2.1',
      description='Data conversor from csv to json, to create the fixtures for django apps',
      url='http://gitlab.csn.uchile.cl/dpineda/csv2json',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPL3',
      packages=['django_csv2json'],
      install_requires=["json", "click", "django"],
      package_dir={'django_csv2json': 'django_csv2json'},
      package_data={
          'datadbs': ['../doc', '../docs', '../requeriments.txt']},
      entry_points={
        'console_scripts':["csv2json = django_csv2json.scripts.csv2json:csv2json",]
        },
      zip_safe=False)
