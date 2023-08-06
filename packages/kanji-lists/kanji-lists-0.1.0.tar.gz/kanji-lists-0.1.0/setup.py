# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kanji_lists']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kanji-lists',
    'version': '0.1.0',
    'description': 'Collection of Japanese kanji lists',
    'long_description': '===========\nKanji Lists\n===========\nA collection of Japanese character lists\n\nInstallation\n============\n\n.. code-block:: console\n\n    pip install kanji-lists\n\n\nUsage\n=====\n\nUsing a list is simple enough:\n\n.. code-block:: pycon\n\n    >>> from kanji_lists import JOYO\n    >>> "桃" in JOYO\n    True\n    >>> "苺" in JOYO\n    False\n    >>> len(JOYO)\n    2136\n\nSome lists also have subordinate lists:\n\n.. code-block:: pycon\n\n    >>> from kanji_lists import KYOIKU\n    >>> "火" in KYOIKU.GRADE1\n    True\n    >>> "火" in KYOIKU.GRADE2\n    False\n    >>> KYOIKU.GRADE1.issubset(KYOIKU)\n    True\n\nLists can also have different versions:\n\n.. code-block:: pycon\n\n    >>> from kanji_lists import KYOIKU\n    >>> KYOIKU.HEISEI4.GRADE6 - KYOIKU.REIWA2.GRADE6\n    {\'城\'}\n    >>> "城" in KYOIKU.REIWA2.GRADE4\n    True\n\nIf you do not specify a version, the default will be chosen. In the case of lists\nmaintained by the Japanese government, this will generally be the most recent list.\nSince the default can change, specify a version if you want to make sure that you\nget the same version of the list across updates.\n\nAvailable Lists and Versions\n============================\n\n\n- JINMEIYO\n    \n  - HEISEI25\n  - HEISEI27\n  - HEISEI29\n- JLPT\n    \n  - TANOS\n            \n    - N1\n    - N2\n    - N3\n    - N4\n    - N5\n- JOYO\n    \n  - HEISEI22\n  - SHOWA56\n- KYOIKU\n    \n  - HEISEI4\n            \n    - GRADE1\n    - GRADE2\n    - GRADE3\n    - GRADE4\n    - GRADE5\n    - GRADE6\n  - REIWA2\n            \n    - GRADE1\n    - GRADE2\n    - GRADE3\n    - GRADE4\n    - GRADE5\n    - GRADE6\n  - SHOWA36\n            \n    - GRADE1\n    - GRADE2\n    - GRADE3\n    - GRADE4\n    - GRADE5\n    - GRADE6\n  - SHOWA55\n            \n    - GRADE1\n    - GRADE2\n    - GRADE3\n    - GRADE4\n    - GRADE5\n    - GRADE6',
    'author': 'Daniel Lemm',
    'author_email': 'daniel.lemm@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffe4/kanji-lists',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
