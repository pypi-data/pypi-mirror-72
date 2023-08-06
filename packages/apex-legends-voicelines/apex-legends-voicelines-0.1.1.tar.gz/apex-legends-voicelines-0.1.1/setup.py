# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apex_legends_voicelines', 'apex_legends_voicelines.assets']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['apex-voicelines = apex_legends_voicelines.__main__:main']}

setup_kwargs = {
    'name': 'apex-legends-voicelines',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Apex Legends voicelines\n\n[[_TOC_]]\n\n## Install\n\nRecommended way to install is by using [pipx](https://github.com/pipxproject/pipx/).\n\nPipx will add isolation so that your system is always unaffected.\n\n```sh\npipx install apex-legends-voicelines\n```\n\n## Usage\n\nTo use just run\n\n```sh\napex-voicelines\n```\n\n### Using inside Emacs\n\nThese voicelines can be used inside Emacs.\n\nYou can use the voicelines as the frame title.\n\n#### As frame title on startup\n\nAdd this to your config\n\n```emacs-lisp\n(setq frame-title-format (shell-command-to-string "apex-voicelines"))\n```\n\n#### Use interactively\n\nYou can also add this in your config and change the title on demand\n\n```emacs-lisp\n(defun change-emacs-title-apex ()\n  (interactive)\n  (setq frame-title-format (shell-command-to-string "apex-voicelines")))\n```\n\nJust run `M-x change-emacs-title-apex` to do so.\n\n## License\n\nMIT License\n',
    'author': 'Justine Kizhakkinedath',
    'author_email': 'justine@kizhak.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://justine.kizhak.com/projects/apex-legends-voicelines',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
