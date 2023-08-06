# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uceasy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['uceasy = uceasy.console:cli']}

setup_kwargs = {
    'name': 'uceasy',
    'version': '0.2.0',
    'description': 'Wrapper for the Phyluce phylogenomics software package',
    'long_description': '<p>\n    <img src="docs/img/uceasy_logo.jpg" height="200px">\n\n</p>\n\n[![Tests](https://github.com/uceasy/uceasy/workflows/Tests/badge.svg)](https://github.com/uceasy/uceasy/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/uceasy/uceasy/branch/master/graph/badge.svg)](https://codecov.io/gh/uceasy/uceasy)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=uceasy_uceasy&metric=alert_status)](https://sonarcloud.io/dashboard?id=uceasy_uceasy)\n\n# UCEasy: a wrapper for the PHYLUCE software package\n\n\n__UCEasy__ is a wrapper to automate manual procedures of the [PHYLUCE](https://phyluce.readthedocs.io/en/latest) software package by abstracting the pipeline steps in only one command, easing the execution and improving reproducibility.\n\n\nAt the moment, the only software for _in silico_ analysis of [ultraconserved elements](https://www.ultraconserved.org/) (UCEs) is Phyluce, but its execution can be quite challenging especially for non-computer experts.\n__UCEasy__ is a convenient tool that automates the execution of common tasks for all types of UCE analysis, these being [Quality Control](https://phyluce.readthedocs.io/en/latest/quality-control.html), [Assembly](https://phyluce.readthedocs.io/en/latest/assembly.html) and [UCE Processing](https://phyluce.readthedocs.io/en/latest/uce-processing.html).\n\n## Installation Guide\n### Dependencies\n* PHYLUCE ^1.6\n\nSee [releases](https://github.com/uceasy/uceasy/releases) for pre-built binaries for Linux (statically linked against [musl libc](https://musl.libc.org/)). Or install it from [PyPI](https://pypi.org/project/uceasy/):\n```\npip install uceasy\n```\nThen, make sure you have a working installation of PHYLUCE, check out the installation guide at [PHYLUCE\'s documentation](https://phyluce.readthedocs.io/en/latest/installation.html).\n\nFor a guide of how to use UCEasy see: [Tutorial](https://github.com/uceasy/uceasy/wiki/Tutorial).\n\n## Acknowledgements\n\nWe thank the following institutions, which contributed to ensuring the success of our work:\n\nMinistério da Ciência, Tecnologia, Inovação e Comunicação (MCTIC)\n\nMuseu Paraense Emílio Goeldi (MPEG)\n\nCentro Universitário do Estado do Pará (CESUPA)\n\n## Funding\n\nThis work has been supported by Conselho Nacional de Desenvolvimento Científico e Tecnológico - CNPq (grants 149985/2018-5; 129954/2018-7).\n\n## Authors\n\n Marcos Paulo Alves de Sousa<br>\n Caio Vinícius Raposo Ribeiro <br>\n Lucas Peres Oliveira <br>\n Romina do Socorro da Silva Batista\n\n ## Contact\n\nDr. Marcos Paulo Alves de Sousa (Project leader)\n\n_Email: **msousa@museu-goeldi.br**_<br>\n_Laboratório de Biologia Molecular_<br>\n_Museu Paraense Emílio Goeldi_<br>\n_Av. Perimetral 1901. CEP 66077- 530. Belém, Pará, Brazil._\n',
    'author': 'Caio Raposo',
    'author_email': 'caioraposo@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://uceasy.github.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
