# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""This is the main module of Lino Amici.

.. autosummary::
   :toctree:

   lib


"""

from os.path import join, dirname
fn = join(dirname(__file__), 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))

__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://amici.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/amici/blob/master/%s'
doc_trees = ['docs']
