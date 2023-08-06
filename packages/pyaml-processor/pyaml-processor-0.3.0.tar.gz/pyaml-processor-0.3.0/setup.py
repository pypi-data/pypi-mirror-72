# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaml_processor']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3,<6.0']

setup_kwargs = {
    'name': 'pyaml-processor',
    'version': '0.3.0',
    'description': 'Library for embedding Python code in YAML.',
    'long_description': '# Python YAML\n\nLibrary for adding Python code in YAML processing\n\nhttps://github.com/gwww/pyaml\n\n## Requirements\n\n- Python 3.6 (or higher)\n\n## Description\n\nDocs are light at this point. Take a look a `example/test.yaml` and associated\nfiles and at `test/test_pyaml.py`.\n\nThis lib is distinguished from other templating languages in that\nindentation, crucial in YAML, is preserved on `include`, `eval`, and `exec`\n\nThis uses python\'s `eval` and `exec` functions. Read about security concerns\nabout use of those. Since this software is not accessing "unaudited" code the\nsecurity risk of using `eval` and `exec` is viewed as low. Never accept/use\nPython code without inspecting the code.\n\n## Installation\n\n```bash\n    $ pip install pyaml\n```\n\n## Overview\n\n`pyaml` reads a YAML file and runs the tagged code inside the YAML file. It \nsupports three processing tags: `eval` to run code, `exec` to load code, and `include` to include other files in the context of the current file. All three\nprocessors are aware of YAML indenting requirements.\n\n### Eval\n\n`eval` is triggered in a YAML file using the tags `@%` to open an `eval` and `%@`\nto close an `eval`. Anything in between the two tags is passed to the Python `eval`\nfunction for processing. Whatever is returned from the `eval` is inserted into\nthe YAML stream. The starting character position of the opening tag is used as\nthe indent level prepended to everything returned.\n\nFor the examples in this section assume that the following Python code\nis in the module `resources.py` and that file contains the following:\n```\nfrom random import randrange\n\n_PATH = "/local/cards/"\n\ndef resources(module, module_type):\n    version = f"?v={randrange(1000000)}"\n    # This works to, the lib can handle lists, dicts, etc as return values:\n    # return [{\'url\': f"{_PATH}/{module}{version}", "type": module_type}]\n    return f"url: {_PATH}/{module}{version}\\ntype: {module_type}"\n```\n\nExample 1:\n```\n@+ from resources import resources +@\nresources:\n  - @% resources("layout-card", "module") %@\n  - @% resources("card-mod", "module") %@\n```\n\nProcessing with `pyaml` results in:\n```\nresources:\n  - url: /local/cards//layout-card?v=238120\n    type: module\n  - url: /local/cards//card-mod?v=885753\n    type: module\n```\n\nNotice that the indentation is preserved from the position on the line where\nthe `eval` was invoked.\n\nNote that the space around the start and end tags is optional.\n\n### Exec\n\n`exec` is triggered in a YAML file using the tags `@%` to open an `eval` and `%@`\nto close an `exec`. Anything in between the two tags is passed to the Python `exec`\nfunction for processing. Whatever is returned from the `exec` is NOT inserted into\nthe YAML stream. The code inside the `exec` tags is `dedent`ed meaning \ncommon leading whitespace on each line is removed.\n\nExample 2:\n```\n@+\ndef markdown_card(label):\n    return \\\nf"""type: markdown\nstyle: |\n  ha-card {{background: purple}}\ncontent: |\n  ## {label}"""\n+@\n\ntitle: My awesome Lovelace config\nviews:\n  - title: Home\n    cards:\n      - @%markdown_card("Kitchen")%@\n      - @%markdown_card("Living room")%@\n```\n\nProcessing with `pyaml` results in:\n```\ntitle: My awesome Lovelace config\nviews:\n  - title: Home\n    cards:\n      - type: markdown\n        style: |\n          ha-card {background: purple}\n        content: |\n          ## Kitchen\n      - type: markdown\n        style: |\n          ha-card {background: purple}\n        content: |\n          ## Living room\n```\n\nNote: any type of Python code may exist between the tags, however,\nit is likely more maintainable to put code, such the code in the\nexample above, into it\'s own Python module.\n\n### Include\n\nIncludes the contents of the file into the YAML stream. The included file\nmay contain `eval` and `exec` blocks. Include is trigged using the same\nopen and closing tag of `@@`.\n\nThe advantage of using `pyaml` include over the include processing from PyYAML\nis that `pyaml` preserves indentation.\n\nFor example if `example3_include.yaml` contains:\n```\n- zoo: tiger\n- moo: cow\n```\n\nAnd the following YAML file:\n```\nbig_pets:\n  @@include some_file.yaml@@\n```\n\nProcessing with `pyaml` results in:\n```\nbig_pets:\n  - zoo: tiger\n  - moo: cow\n```\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for development dependencies. Installation instructions are on their website.\n\nTo get started developing:\n\n```\ngit clone https://github.com/gwww/pyaml.git\ncd pyaml\npoetry install\npoetry shell # Or activate the created virtual environment\npytest # to ensure everything installed properly\n```\n\nThere is a `Makefile` in the root directory as well. The `make` command\nfollowed by one of the targets in the `Makefile` can be used. If you don\'t\nhave or wish to use `make` the `Makefile` serves as examples of common\ncommands that can be run.\n',
    'author': 'Glenn Waters',
    'author_email': 'gwwaters+pyaml@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gwww/pyaml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
