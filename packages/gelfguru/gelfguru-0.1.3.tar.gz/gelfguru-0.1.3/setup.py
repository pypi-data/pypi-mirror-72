# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gelfguru']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'gelfguru',
    'version': '0.1.3',
    'description': 'Loguru extension for log in GELF payload format.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/gelfguru.svg)](https://badge.fury.io/py/gelfguru)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ecc1f25454164ff78e432f5a126563cb)](https://www.codacy.com/manual/augustoliks/loguru-gelf-extension?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=augustoliks/loguru-gelf-extension&amp;utm_campaign=Badge_Grade)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n# gelfguru\n\nA Loguru extension for handling log messages and adapt to GELF payload pattern, without modifying  built-in Loguru methods call.\nThis library was created especially for applications running in Docker environment with GELF Logging Driver.\n\nFeatures:\n- Dont modify call methods Loguru, like `logger.trace`, `logger.info`, `logger.info` etc;\n- Create new methods for `logger` instance, with all [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity level;\n- Associates [RFC-5424](https://en.wikipedia.org/wiki/Syslog) Severity Levels Numerical Codes in GELF field.\n- Filter logs by environment variable `GELFGURU_LEVEL`.\n\n# Installation\n\n```shell\npip3.7 install gelfguru\n```\n\n# How to Use \n\nIf you configure Loguru instance with `gelfguru`, you only need to execute:\n\n```python\nfrom loguru import logger\nfrom gelfguru import configure_gelf_output\n\nconfigure_gelf_output()\n\nlogger.trace(\'loguru trace calls equals gelfguru debug calls\')\nlogger.info(\'Numeric level RFC-5424\')\nlogger.emergency(\'Implemented RFC-5424 Syslog Severity Logs\')\n```\n\n## Log Levels\n\nGELF log level is equal to the standard syslog levels.\n\n| gelfluru             | Syslog Severity  | Numerical Code   | Description\n|:---:                 |:---:             | :---:            | :---:\n|  `emergency`         | Emergency        | 0                | System is unusable. A panic condition\n|  `alert`             | Alert            | 1                | Action must be taken immediately. A condition that should be corrected immediately, such as a corrupted system database.[\n|  `critical`          | Critical         | 2                | Critical conditions. Hard device errors\n|  `error`             | Error            | 3                | Error conditions. \n|  `warning`           | Warning          | 4                | Warning conditions\n|  `success`, `notice` | Notice           | 5                | Normal but significant condition. Conditions that are not error conditions, but that may require special handling\n|  `info`              | Informational    | 6                | Informational messages\n|  `debug`, `trace`    | Debug            | 7                | Debug-level messages. Messages that contain information normally of use only when debugging a program.\n\nExample:\n\n```python\nfrom loguru import logger                                                                             \nfrom gelfguru import configure_gelf_output                                                            \n\nconfigure_gelf_output()                                                                               \n\nlogger.trace(\'loguru trace calls equals gelfguru debug calls\')                                        \n# {\n#   "version": "1.1",\n#   "short_message": "trace\\n",\n#   "full_message": "trace\\n",\n#   "timestamp": 1593137655.309429,\n#   "level": 7,\n#   "line": 1,\n#   "_file": "<ipython-input-4-698cb139534b>",\n#   "_context": {\n#     "module": "__main__:<module>:1",\n#     "process": "MainProcess",\n#     "thread": "MainThread"\n#   }\n# }\n\nlogger.info(\'Change numeric level value, in the case, is used RFC-5424 numeric level value\')          \n# {\n#   "version": "1.1",\n#   "short_message": "Change numeric level value, in the case, is used RFC-5424",\n#   "full_message": "Change numeric level value, in the case, is used RFC-5424 numeric level value",\n#   "timestamp": 1593137655.42884,\n#   "level": 6,\n#   "line": 1,\n#   "_file": "<ipython-input-5-d527b5b194dc>",\n#   "_context": {\n#     "module": "__main__:<module>:1",\n#     "process": "MainProcess",\n#     "thread": "MainThread"\n#   }\n# }\n\nlogger.emergency(\'Implemented RFC-5424 Syslog Severity Logs\')                                         \n# {\n#   "version": "1.1",\n#   "short_message": "Implemented RFC-5424 Syslog Severity Logs",\n#   "full_message": "Implemented RFC-5424 Syslog Severity Logs",\n#   "timestamp": 1593137657.236526,\n#   "level": 0,\n#   "line": 1,\n#   "_file": "<ipython-input-6-5c45ca4c1de6>",\n#   "_context": {\n#     "module": "__main__:<module>:1",\n#     "process": "MainProcess",\n#     "thread": "MainThread"\n#   }\n# }\n\nlogger.bind(new_field="i am additional filed gelf").error(\'iste natus error sit\')\n# {\n#   "version": "1.1",\n#   "short_message": "iste natus error sit",\n#   "full_message": "iste natus error sit",\n#   "timestamp": 1593138435.430722,\n#   "level": 3,\n#   "line": 18,\n#   "_file": "/home/augustoliks/github/loguru-gelf-extension/tests/test_loguru_gelf_extension.py",\n#   "_context": {\n#     "module": "test_loguru_gelf_extension:test_loguru_calls:18",\n#     "process": "MainProcess",\n#     "thread": "MainThread"\n#   },\n#   "_new_field": "i am additional filed gelf"\n# }\n```',
    'author': 'Carlos Neto',
    'author_email': 'carlos.santos110@fatec.sp.gov.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/augustoliks/loguru-gelf-extension/tree/develop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
