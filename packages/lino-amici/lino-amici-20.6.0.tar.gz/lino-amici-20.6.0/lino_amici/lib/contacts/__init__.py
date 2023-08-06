# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Lino Amici extension of :mod:`lino_xl.lib.contacts`.

"""

from lino_xl.lib.contacts import Plugin


class Plugin(Plugin):
    
    extends_models = ['Person', 'Company']

    use_vcard_export = True
    
