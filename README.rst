drand.py
========

.. image:: https://img.shields.io/pypi/v/drand.svg
         :target: https://pypi.python.org/pypi/drand

.. image:: https://img.shields.io/travis/initc3/drand.py.svg
         :target: https://travis-ci.com/initc3/drand.py

.. image:: https://img.shields.io/codecov/c/github/initc3/drand.py
         :target: https://codecov.io/gh/initc3/drand.py
         :alt: Codecov

.. image:: https://readthedocs.org/projects/drandpy/badge/?version=latest
         :target: https://drandpy.readthedocs.io/en/latest/?badge=latest
         :alt: Documentation Status

.. image:: https://img.shields.io/badge/ic3-powered-9c2a4c
         :target: https://www.initc3.org/projects.html
         :alt: IC3 Powered

Python client to query a `drand`_ network for publicly verifiable,
unbiased, and unpredictable random values.

To learn more about `drand`_ see `drand's
documentation <https://github.com/drand/drand#documentation>`_.

**WARNING: This software is currently only, strictly, and purely for
experimental purposes. It was developed for prototyping and
experimenting with the** `drand`_ **network, which is itself still
experimental!**

**IMPORTANT**: Currently only works with the `drand`_ server code
from the ``master`` branch (as of March 8, 2020). To query the `drand
test network`_ (e.g.: `League of Entropy`_) using Python you may try
`drb-client`_.

.. contents::
    :local:
    :depth: 3


.. _install:

Install
-------
.. code-block:: shell

   $ pip install drand

.. _usage:

Usage
-----
Prerequisite: Run a local drand network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
First, run a local drand network. See `devnet/README.md`_ for
more details.

.. code-block:: shell

   $ cd devnet
   $ ./run.sh

**Get the addresses of the drand servers**

.. code-block:: python

   from drand.utils import get_addresses_from_group_file

   group_file = 'devnet/data/group.toml'
   addresses = get_addresses_from_group_file(group_file)

.. code-block:: python

   >>> addresses
   ['172.15.238.2:8084',
    '172.15.238.3:8081',
    '172.15.238.4:8080',
    '172.15.238.6:8082',
    '172.15.238.5:8083']

Query a drand server
^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

   import drand

Get the public key of the network (/api/info/distkey)
"""""""""""""""""""""""""""""""""""""""""""""""""""""
Each node has a public share of this group key.

.. code-block:: python

   distkey = await drand.get_distkey(addresses[0], tls=False)

.. code-block:: python

   >>> distkey
   '9509e2c2a5d04776bedce40839341375c89aa34a0372a1db273f562d89050b4ae54a76a276a26580166b0cd91e63f909'

Get and verify a random value (/api/public)
"""""""""""""""""""""""""""""""""""""""""""
The verification means verifying that the "randomness" value is
the hash of the signature, and that the signature is valid for the
public key (distkey) and the the message (round + previous)

.. code-block:: python

   res = await drand.get_and_verify(
       addresses[3], distkey=distkey, tls=False,
   )

.. code-block:: python

   >>> res
   {'round': 73,
    'previous': 'b894ccc3859d1fb6d2ce6722b7195d359fbe6b0a387a3693e539e4957f1c69025936919fff3bd89a303ccfbcb929aae10eb68172997bdc84ccc6295dd21903a77994a116e203514935e9e25bf3f830cb00e6546470260f9beab65a5e389050bd',
    'signature': '817254f9267e5345f5160a794ad5ffca0a9a2295cbfedc8c3d19215f91c8ccd07faa8354564d18159905477757c21f8a05140761ab5eb7b1d622ef5b62d64cdecf7f5c1e3d06d7ac016e16c4bfaddc4b27985625d32cd73e650e8fb7ea8dccf0',
    'randomness': '66c3554bc0927a4ccbfdd73856071be792e3ddec7c27193d2f2f4d482c78b6b2'}

**Get a random value for round 5**

.. code-block:: python

   res = await drand.get_and_verify(
       addresses[3], distkey=distkey, tls=False, round_=5
   )

.. code-block:: python

   >>> res
   {'round': 5,
    'previous': 'aab94951afa626c26af5e08baa111fb98b1f5300556dc472f5e976a1ca4ccb074ecb7778cf18e08272fb40e1421a630914fe178ff1353d1247f58ecf4b82c417a55b8867e1f6eca4ca4bc548db2c2d1ce31c52e34f97c7f001774dc3fb6f22d5',
    'signature': 'ad3e4f0bf0ef93c2ced95c12e1e7b5d0adbc4791e5592a83ce6119e0b610b7de40786e639861aa62df9d3a01b0ac50f90c84b1b20c5cc0662774c324f03fda0a69f0625a54a0c4c066f3b441cb33a8782f88d53861a5d4d8035a96488e340141',
    'randomness': 'baee3fd77cd09349325794f766c0c81c887987907ec2834ac09a8a46c2193747'}

**Get random values for a range of rounds**

.. code-block:: python

   import asyncio

   from aiohttp import ClientSession

   async def get_rands(rounds):
       async with ClientSession() as session:
           tasks = []
           for r in rounds:
               tasks.append(
                   drand.get_and_verify(
                       addresses[4],
                       distkey=distkey,
                       session=session,
                       tls=False,
                       round_=r,
                   )
               )
           rands = await asyncio.gather(*tasks)
       return rands

.. code-block:: python

   >>> asyncio.run(get_rands(range(2, 5)))
   [{'round': 2,
     'previous': 'b816229db70d3d7ab727bf0dc8ae3de27c354b066d5d931d3b6fb14d2fcf2433cd72f0271a9c47e7448de7c9589de2250d85ad444175cb616ca6fa0f6f0d376e608378c3688ee528631132c3c7928dfcec9f302a91daac51f1e87c98ebff78d5',
     'signature': 'a515fe873dc18810d3aa446614786aa63567930f888c82b1edf66ea1e0f604c46948863dc349320219eba7d11a784813152719f0d6d471a08227c27393d14eb02a8df7c18cb48f5df6918510948e6170922ad5164da0965c47b63ba80ee7a682',
     'randomness': '185963dba81d25158bb60bc0bc16823b7687a87cca739a6a9e4a2bccac16c5f0'},
    {'round': 3,
     'previous': 'a515fe873dc18810d3aa446614786aa63567930f888c82b1edf66ea1e0f604c46948863dc349320219eba7d11a784813152719f0d6d471a08227c27393d14eb02a8df7c18cb48f5df6918510948e6170922ad5164da0965c47b63ba80ee7a682',
     'signature': '81d3a98e63e8480d61e64ef7126dea5f83cc98303d43c66221f15edab8dc4e02d7c229a645f107ee76e0de11673569810f18fc6fd5d27e5a50aa0cbf95e90f1d6c750715a9e4b79ec8a5982421e2a324864d1471e36a0af3c773864923a3e3b4',
     'randomness': '0b7d6c4a465b4cd6099f4a888ea355c2173a8108ad749a7790c64592a9c2ee9f'},
    {'round': 4,
     'previous': '81d3a98e63e8480d61e64ef7126dea5f83cc98303d43c66221f15edab8dc4e02d7c229a645f107ee76e0de11673569810f18fc6fd5d27e5a50aa0cbf95e90f1d6c750715a9e4b79ec8a5982421e2a324864d1471e36a0af3c773864923a3e3b4',
     'signature': 'aab94951afa626c26af5e08baa111fb98b1f5300556dc472f5e976a1ca4ccb074ecb7778cf18e08272fb40e1421a630914fe178ff1353d1247f58ecf4b82c417a55b8867e1f6eca4ca4bc548db2c2d1ce31c52e34f97c7f001774dc3fb6f22d5',
     'randomness': '2dcc3e4894c91d092cdbcbe6daf777c5cbe2e6948cf8a18693009762273d52aa'}]

.. _acks:

Acknowledgments
---------------
The initial code interface for this package was based on the
JavaScript client `drandjs`_.

The ``devnet`` directory under the root of the `repo`_ was taken
from the `demo`_ directory under the `drand/drand`_ repository, tree
with commit hash `a40dc25e1aec6822a79c72b4aaca12e65c700f01`_. The
code was brought over using `git-filter-repo`_ in order to preserve the
commit history.

The original boilerplate for this package was created with
Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project
template.

Thanks to `IC3`_ (The Initiative For Cryptocurrencies & Contracts) for
supporting this work.


Reminder & Future Work
----------------------
**This software is currently only, strictly, and purely for
experimental purposes. It was developed for prototyping and
experimenting with the** `drand`_ **network, which is itself still
experimental!**

The `Github issue tracker`_ will be used to plan and manage future
work.


.. _drand: https://github.com/drand/drand
.. _drand test network: https://drand.github.io/
.. _league of entropy: https://www.cloudflare.com/leagueofentropy/
.. _drb-client: https://github.com/Snawoot/drb-client
.. _devnet/README.md: https://github.com/initc3/drand.py/blob/master/devnet/README.md
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _drandjs: https://github.com/drand/drandjs
.. _repo: https://github.com/initc3/drand.py
.. _git-filter-repo: https://github.com/newren/git-filter-repo
.. _demo: https://github.com/drand/drand/tree/a40dc25e1aec6822a79c72b4aaca12e65c700f01/demo
.. _drand/drand: https://github.com/drand/drand
.. _a40dc25e1aec6822a79c72b4aaca12e65c700f01: https://github.com/drand/drand/tree/a40dc25e1aec6822a79c72b4aaca12e65c700f01/demo
.. _Github issue tracker: https://github.com/initc3/drand.py/issues
.. _ic3: https://www.initc3.org/
