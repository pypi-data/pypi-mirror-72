# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sheetsql']

package_data = \
{'': ['*']}

install_requires = \
['gspread>=3.6.0,<4.0.0',
 'regex>=2020.6.8,<2021.0.0',
 'requests>=2.24.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'sheet-sql',
    'version': '0.1.0',
    'description': 'SQL for Google Sheets',
    'long_description': '# sheet-sql\n\n[![Build](https://github.com/andyh1203/sheet-sql/workflows/ci/badge.svg)](https://github.com/andyh1203/sheet-sql/actions?workflow=ci)\n[![Codecov](https://codecov.io/gh/andyh1203/sheet-sql/branch/master/graph/badge.svg)](https://codecov.io/gh/andyh1203/sheet-sql)\n[![PyPI](https://img.shields.io/pypi/v/sheet-sql.svg)](https://pypi.org/project/sheet-sql/)\n[![Read the Docs](https://readthedocs.org/projects/sheet-sql/badge/)](https://sheet-sql.readthedocs.io/)\n\nsheet-sql allows for writing SQL-style queries to query data from Google Sheets.\nIt makes use of Google\'s Table Query (tq) Language. See [here](https://developers.google.com/chart/interactive/docs/querylanguage) for more details.\n\n    >>> from sheetsql import connect\n    >>> gs = connect("service_account")\n    >>> gs.spreadsheets\n    [<Spreadsheet \'Test\' id:1z2917zfaUqeE9-fMn-XAUvDwzQ8Q_2rEXHRst5KZC3I>, <Spreadsheet \'my new spreadsheet\' id:1I4pfBHYoY_ajW13Tn8t2-AyqmWK1HzcJPccyRUefdyw>]\n    >>> spreadsheet = gs[\'1z2917zfaUqeE9-fMn-XAUvDwzQ8Q_2rEXHRst5KZC3I\']\n    >>> spreadsheet\n    <Spreadsheet \'Test\' id:1z2917zfaUqeE9-fMn-XAUvDwzQ8Q_2rEXHRst5KZC3I>\n    >>> spreadsheet.worksheets\n    [\'Sheet1\', \'Sheet2\']\n    >>> worksheet = spreadsheet[\'Sheet1\']\n    >>> worksheet\n    <Worksheet \'Sheet1\' id:0>\n    >>> worksheet.columns\n    [\'test\', \'test2\', \'test3\']\n    >>> query = worksheet.query("SELECT *")\n    <generator object Worksheet._result_handler.<locals>.<genexpr> at 0x7fe86c3c2840>\n    >>> for row in query:\n    ...   print(row)\n    ...\n    {\'test\': 1.0, \'test2\': 6.0, \'test3\': 11.0}\n    {\'test\': 2.0, \'test2\': 7.0, \'test3\': 12.0}\n    {\'test\': 3.0, \'test2\': 8.0, \'test3\': 13.0}\n    {\'test\': 4.0, \'test2\': 9.0, \'test3\': 14.0}\n    {\'test\': 5.0, \'test2\': 10.0, \'test3\': 15.0}\n    >>> worksheet.default_row_type\n    <class \'dict\'>\n    >>> worksheet.default_row_type = list\n    >>> worksheet.default_row_type\n    <class \'list\'>\n    >>> query = worksheet.query("SELECT *")\n    >>> for row in query:\n    ...   print(row)\n    ...\n    [1.0, 6.0, 11.0]\n    [2.0, 7.0, 12.0]\n    [3.0, 8.0, 13.0]\n    [4.0, 9.0, 14.0]\n    [5.0, 10.0, 15.0]\n\nTo install, run\n\n    pip install sheet-sql\n\nAlternatively, install with [poetry](https://python-poetry.org/)\n\n    poetry add sheet-sql\n',
    'author': 'Andy Huynh',
    'author_email': 'andy.huynh312@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andyh1203/sheet-sql',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
