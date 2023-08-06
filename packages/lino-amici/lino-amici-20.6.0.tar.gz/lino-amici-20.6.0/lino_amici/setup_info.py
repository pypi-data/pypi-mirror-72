# -*- coding: UTF-8 -*-
# Copyright 2017-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# $ python setup.py test -s tests.PackagesTests.test_packages

SETUP_INFO = dict(
    name='lino-amici',
    version='20.6.0',
    install_requires=['lino-xl', 'vobject', 'lino-react'],

    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("A Lino application for managing family contacts"),
    long_description="""\

Lino Amici is a customizable Lino application for managing family
contacts.  It is currently a submarine project, used only by its
author and therefore poorly documented.

- The central project homepage is http://amici.lino-framework.org

- For *introductions* and *commercial information* about Lino Amici
  please see `www.saffre-rumma.net
  <http://www.saffre-rumma.net>`__.


""",
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="http://amici.lino-framework.org",
    license='BSD-2-Clause',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
Topic :: Communications :: Email :: Address Book
Topic :: Office/Business :: Groupware
""".splitlines())

SETUP_INFO.update(packages=[str(n) for n in """
lino_amici
lino_amici.lib
lino_amici.lib.amici
lino_amici.lib.amici.fixtures
lino_amici.lib.contacts
lino_amici.lib.contacts.fixtures
lino_amici.projects
lino_amici.projects.amici1
lino_amici.projects.amici1.settings
lino_amici.projects.amici1.settings.fixtures
lino_amici.projects.amici1.tests
lino_amici.lib.users
lino_amici.lib.users.fixtures
""".splitlines() if n])

SETUP_INFO.update(message_extractors={
    'lino_amici': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(include_package_data=True, zip_safe=False)
# SETUP_INFO.update(package_data=dict())


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l

# l = add_package_data('lino_noi.lib.noi')
# for lng in 'de fr'.split():
#     l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
