# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['secrets_tool', 'secrets_tool.handlers']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.9.2,<3.0.0', 'ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['secrets_tool = secrets_tool.__main__:main']}

setup_kwargs = {
    'name': 'secrets-tool',
    'version': '0.1.0',
    'description': 'A lightweight tool to easily encrypt/decrypt secrets inside a repository',
    'long_description': "# Secrets Tool\nThis is a small tool which helps to encrypt secrets that must be committed to a Git repository.\n\nIt has the advantage to natively support partial encryption of YAML files. This is of great advantage, as it allows to see the YAML file structure even when some of its contents are encrypted (your PR reviewers and diff tools will thank you)\n\n## Prerequisites\n* Python >= 3.7\n* Having the following packages installed: `pip install ruamel.yaml cryptography`\n\n## Usage\nThe tool reads a list of files to encrypt/decrypt from a `.gitignore` file. In there it will only consider files that are sorrounded by a comment block as in the following example:\n\n```\n# BEGIN ENCRYPTED\nkaas-rubik-stage/values.yaml\n# END ENCRYPTED\n```\n\nRun the tool by giving the `.gitignore` file as an argument, together with either a `encrypt` or `decrypt` command:\n\n```\ncd <REPOSITORY_ROOT>\npython -m utils.secrets_tool k8s_helm/.gitignore encrypt\n```\n\n## Syntax\nThe tool provides different encryption handlers for all kind of file types.\n* `yaml` for YAML files that are used by tools which are okay having a `!decrypted` tag in front of strings\n* `yamlcompat` for tools that don't like the additional 'encryption marker' tag.\n* `generic` for all other file types. It encrypts the complete file.\n\nThe desired encryption handler is inferred from the filetype - or it can be given explicitly in the gitignore file using the `# type:` hint:\n\n```\n# BEGIN ENCRYPTED\nkaas-rubik-stage/values.yaml\n\n# type: yaml\nkaas-rubik-stage/values2.txt\n# END ENCRYPTED\n```\n\n### yamlcompat\nThis encryption handler can encrypt individual YAML keys without relying on 'parser visible' changes in the YAML file structure.\nInstead of marking the desired keys directly in the file, they are listed in the .gitignore file using a `# data: ` comment:\n\n```\n# BEGIN ENCRYPTED\nkaas-rubik-stage/values.yaml\n\n# type: yamlcompat\n# data: splunk.apiToken\n# data: splunk.host\nkaas-rubik-stage/values2.yaml\n# END ENCRYPTED\n```\n\n*WARNING* It is recommended to use the normal YAML handler whenever possible. When using the yamlcompat module, you split up your encryption logic over multiple files, which might lead to errors (especially on fragile YAML files that contain unnamed structures - like lists)\n",
    'author': 'Alexander Hungenberg',
    'author_email': 'alexander.hungenberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/defreng/secrets-tool',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
