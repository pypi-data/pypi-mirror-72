# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['i3_balance_workspace']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['i3_balance_workspace = i3_balance_workspace:main']}

setup_kwargs = {
    'name': 'i3-balance-workspace',
    'version': '1.7.0',
    'description': 'Balance windows and workspaces in i3wm',
    'long_description': '# i3-balance-workspace\n\n[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/atreyasha/i3-balance-workspace?color=brightgreen&label=release&logo=GitHub)](https://github.com/atreyasha/i3-balance-workspace/tags)\n[![PyPI](https://img.shields.io/pypi/v/i3-balance-workspace?color=brightgreen&logo=pypi&logoColor=yellow)](https://pypi.org/project/i3-balance-workspace/)\n[![AUR version](https://img.shields.io/aur/version/i3-balance-workspace?color=brightgreen&logo=Arch%20Linux)](https://aur.archlinux.org/packages/i3-balance-workspace/)\n\nBalance windows and workspaces in i3wm. Functionality is similar to the `Emacs` command `M-x balance-windows`.\n\n## Installation\n\nFollowing are available options to install `i3-balance-workspace`:\n\n1. Install from PyPi (Python Package Index) using `pip`:\n\n    ```shell\n    $ pip install i3-balance-workspace\n    ```\n\n2. For Arch-Linux users, install `i3-balance-workspace` via the [AUR](https://aur.archlinux.org/packages/i3-balance-workspace/).\n\n3. To install locally, ensure `poetry` and `pip` are installed on your system. Then execute:\n\n    ```shell\n    $ make install\n    ```\n\n## Usage\n\n```\nusage: i3_balance_workspace [-h] [--scope {workspace,focus}] [--timeout <int>]\n\noptional arguments:\n  -h, --help  show this help message and exit\n  --scope     {workspace,focus}\n              scope of resizing containers (default: workspace)\n  --timeout   <int>\n              timeout in seconds for resizing (default: 1)\n```\n\nIn order to balance all windows in the current workspace, simply execute:\n\n```shell\n$ i3_balance_workspace\n```\n\nAlternatively, it is possible to only balance the windows that are in focus. For this, execute the following:\n\n```shell\n$ i3_balance_workspace --scope focus\n```\n\nIn order to get the full benefit of this routine, it is recommended to initialize i3 persistent keybindings. Below are example keybindings which can be appended to your i3 `config` file.\n\n```shell\nbindsym $mod+b exec "i3_balance_workspace --scope focus"\nbindsym $mod+Shift+b exec "i3_balance_workspace"\n```\n\n## Examples\n\n`i3-balance-workspace` has been tested and shows good performance on both simple and complex workspace layouts. Take a look at some examples:\n\n### Scope: Workspace\n\n<p align="center">\n<img src="https://raw.githubusercontent.com/atreyasha/i3-balance-workspace/master/img/workspace.gif" width="800">\n</p>\n\n### Scope: Focused windows\n\n<p align="center">\n<img src="https://raw.githubusercontent.com/atreyasha/i3-balance-workspace/master/img/windows.gif" width="800">\n</p>\n\n## Bugs\n\nIn case of any bugs, feel free to open a GitHub issue.\n\n## Developments\n\nFurther developments to this repository are summarized in our [change-log](https://github.com/atreyasha/i3-balance-workspace/blob/master/docs/todos.md).\n',
    'author': 'Atreya Shankar',
    'author_email': '35427332+atreyasha@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/atreyasha/i3-balance-workspace',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
