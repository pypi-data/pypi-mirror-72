# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lihzahrd',
 'lihzahrd.bestiary',
 'lihzahrd.chests',
 'lihzahrd.enums',
 'lihzahrd.fileutils',
 'lihzahrd.header',
 'lihzahrd.items',
 'lihzahrd.journeypowers',
 'lihzahrd.npcs',
 'lihzahrd.pressureplates',
 'lihzahrd.signs',
 'lihzahrd.tileentities',
 'lihzahrd.tiles',
 'lihzahrd.townmanager']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lihzahrd',
    'version': '2.0.0',
    'description': 'A Terraria world parser in Python',
    'long_description': '# ![](https://gamepedia.cursecdn.com/terraria_gamepedia/e/ee/Lihzahrd.png?version=b8e7ea78b2f9f27a46e2e70d5684b344) `lihzahrd` [![](https://img.shields.io/pypi/v/lihzahrd)](https://pypi.org/project/lihzahrd/)\n\nA Terraria 1.4.0.5 world parser in Python.\n\nYou can use this package to get programmer-friendly data from a Terraria world!\n\nInstall with:\n```\npip install lihzahrd\n```\n\n## Usage\n\nYou can open a world file and get a `World` object by calling:\n\n```\nimport lihzahrd\nworld = lihzahrd.World.create_from_file("filename.wld")\n```\n\nIt _will_ take a while to process: a small Terraria world contains more than 5 million tiles!\n\nOnce you have a `World` object, you can use all data present in the save file by accessing [its attributes](http://gh.steffo.eu/lihzahrd/html/world.html).\n\n## Documentation\n\nThe documentation is available [here](https://gh.steffo.eu/lihzahrd/html/).\n\nIt\'s a bit messy and incomplete, as I still have not figured out the meaning of some data, and the code is in need of some refactoring.\n\nIf you know something that isn\'t present in the documentation, please let me know [with an issue](https://github.com/Steffo99/lihzahrd/issues/new)!\n\n## PyPy\n\n`lihzahrd` is compatible with [PyPy](https://www.pypy.org), a faster implementation of Python!\n\nIf you think that parsing a world takes too much time, you can use PyPy to reduce the required time by a factor of ~3!\n\n### Benchmarks\n\nTime to parse the same large world:\n\n- CPython took 11.45 s.\n- Pypy took 3.57 s!\n\n## Development\n\nTo contribute to `lihzahrd`, you need to have [Poetry](https://poetry.eustace.io/) installed on your PC.\n\nAfter you\'ve installed Poetry, clone the git repo with the command:\n\n```\ngit clone https://github.com/Steffo99/lihzahrd\n```\n\nThen enter the new directory:\n\n```\ncd lihzahrd\n```\n\nAnd finally install all dependencies and the package:\n\n```\npoetry install\n```\n\nThis will create a new virtualenv for the development of the library; you can activate it by typing:\n\n```\npoetry shell\n```\n\nPlease note that for compatibility with PyPy, the project needs to target Python 3.6.\n\n### Building docs\n\nYou can build the docs by entering the `docs_source` folder and running `make html`, then committing the whole `docs` folder.\n\n## References used\n\n- The [TEdit World Parser](https://github.com/TEdit/Terraria-Map-Editor/blob/master/TEditXna/Terraria/World.FileV2.cs), the most accurate source currently available.\n- The [tModLoader wiki](https://github.com/tModLoader/tModLoader/wiki), containing lists of all possible IDs.\n- The [Terrafirma world documentation](http://seancode.com/terrafirma/world.html), accurate for old worlds (version <69)\n- The [1.3.x.x world documentation](http://ludwig.schafer.free.fr/), a bit incomplete, but an useful source nevertheless.\n- A [JS World Parser](https://github.com/cokolele/terraria-world-parser/) on GitHub.\n- A [Background Guide](https://steamcommunity.com/sharedfiles/filedetails/?id=841032800) on Steam that displays all possible world backgrounds.\n\n## License\n\n`lihzahrd` is licensed under the [AGPL 3.0](/LICENSE.txt).\nThat means you have to publish under the same license the source code of any program you create that uses `lihzahrd`.\n\n## See also\n\n- [flyingsnake](https://github.com/Steffo99/flyingsnake), a map renderer using this package\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/lihzahrd',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
