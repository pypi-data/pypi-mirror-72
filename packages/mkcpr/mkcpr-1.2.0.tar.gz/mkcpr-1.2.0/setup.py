# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkcpr']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mkcpr = mkcpr.main:main']}

setup_kwargs = {
    'name': 'mkcpr',
    'version': '1.2.0',
    'description': 'mkcpr is a command line utility that helps you to build your Competitive Programming Reference in PDF.',
    'long_description': '\n\n# mkcpr &middot; [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/searleser97/mkcpr/blob/master/LICENSE) [![PyPI version fury.io](https://badge.fury.io/py/mkcpr.svg)](https://pypi.org/project/mkcpr/)\n\n### Competitive Programming Reference Builder Tool\n\n## About\n\n```mkcpr``` is a command line utility written in python that helps you to build your *Competitive Programming Reference* in PDF.\n\nThis command will generate a LaTex formatted file, which will be ready to be compiled into your new *Competitive Programming Reference*, using any online or local LaTex compiler of your preference.\n## Usage\n\n- In your working directory run:\n\n```shell\nmkcpr [-c|-h]\n```\n**Notes:**\n\n- The configuration file ```mkcpr-config.json``` should be in the same working directory. (Same path where you run ```mkcpr```).\n- ```-c``` flag creates a new configuration file ```mkcpr-config.json``` in the current directory.\n- ```-h``` displays help.\n\n## Requirements\n\n- python 3.5+\n- Online or local LaTex compiler\n- Folder containing your codes for programming competitions\n- LaTex template (you can use the one provided in this repository ```Example/Template.tex```)\n- Configuration File ```mkcpr-config.json``` (described below)\n\n## Installation\n\n1. Run:\n  ```shell\n    pip install mkcpr --user\n  ```\n2. Copy the LaTex template ```Template.tex``` located in the ```Example``` folder of this repository to your working directory.\n3. In your working directory run ```mkcpr -c``` to create a new configuration file ```mkcpr-config.json```.\n4. Update ```mkcpr-config.json``` and ```Template.tex``` according to your needs. See the [Configuration file options](#configuration-file-options) section for reference.\n5. You are now ready to run ```mkcpr``` in your working directory.\n\n## Configuration File Options\n\n```jsonc\n{\n  "code_folder": "/home/san/Projects/mkcpr/Example/CodeFolder", // Path to your actual code for reference\n  "template_path": "/home/san/Projects/mkcpr/Example/Template.tex", // LaTex template path\n  "output_file_path": "/home/san/Projects/mkcpr/Example/Output.tex", // path where you want the generated LaTex code to be\n  "excluded": ["__pycache__", ".vscode"], // folders not to consider\n  "columns": 2, // number of columns in your reference\n  "template_placeholder": "CODE HERE", // text to replace in your template\n  "sort_before": ["Data Structures"], // files or folders will appear first\n  "sort_after": ["Extras"], // file or folders will appear at the end\n}\n```\n\n## Features\n\n- One single command and your reference will be ready to compile\n- Build it with your own style\n- support for most file extensions. (.cpp, .py, .java, .tex, .sh, ...)\n- Build your reference just from your competitive programming code folder.\n\n<table>\n  <tr>\n    <th> Folder Structure </th>\n    <th> Table Of Contents </th>\n  </tr>\n  <tr>\n    <td>\n      <img src="https://codeforces.com/predownloaded/43/53/4353216697913b06f2909ee25b7d7fe586133501.png"/>\n    </td>\n    <td>\n      <img src="https://codeforces.com/predownloaded/35/f5/35f510c1d145e2f3fb9fb147fcbf3febdff3ddf2.png"/>\n    </td>\n  </tr>\n</table>\n\n- Forget about undesired line breaks by specifying the lines of code you want together in the same page with a single comment before your lines of code.\n\n<table>\n  <tr>\n    <td colspan="2">\n      <img src="https://codeforces.com/predownloaded/29/ea/29ea463f8ac652c6bb5fa20fc1c7690546479333.png"/>\n    </td>\n  </tr>\n  <tr>\n    <td>\n      <img src="https://codeforces.com/predownloaded/a1/4f/a14f0a93f62f3afb7d3519779c18d7e991948ed7.png" width="400" height="250"/>\n    </td>\n    <td>\n      <img src="https://codeforces.com/predownloaded/f6/1e/f61ec142697979d7ebb5b3ec715e2856ebc2faaf.png" width="400" height="250"/>\n    </td>\n  </tr>\n</table>\n\n## Example\n\nYou can see an example of how a working directory would look like in a real *Competitive Progamming Reference* [HERE](https://github.com/searleser97/competitive-programming-reference)\n\n## License\n\n```mkcpr``` is licensed under the [GNU General Public License v3.0](https://github.com/searleser97/mkcpr/blob/master/LICENSE)',
    'author': 'searleser97',
    'author_email': 'serchgabriel97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/searleser97/mkcpr',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
