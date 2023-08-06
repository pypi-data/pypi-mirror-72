from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='django_csv2json',
      version='0.3.0',
      description='Data conversor from csv to json, to create the fixtures for django apps',
      url='https://www.gitlab.com/pineiden/csv-2-json',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPL3',
      packages=['django_csv2json'],
      install_requires=["ujson", "click", "django"],
      package_dir={'django_csv2json': 'django_csv2json'},
      package_data={
          'datadbs': ['../doc', '../docs', '../requeriments.txt']},
      entry_points={
        'console_scripts':["csv2json = django_csv2json.scripts.csv2json:csv2json",]
        },
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
