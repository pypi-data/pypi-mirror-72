# This file is part of caucase
# Copyright (C) 2017-2020  Nexedi SA
#     Alain Takoudjou <alain.takoudjou@nexedi.com>
#     Vincent Pelletier <vincent@nexedi.com>
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.

from setuptools import setup, find_packages
import versioneer

with open("README.rst") as readme, open("CHANGES.txt") as changes:
  long_description = readme.read() + "\n" + changes.read() + "\n"

setup(
  name='caucase',
  version=versioneer.get_version(),
  cmdclass=versioneer.get_cmdclass(),
  author='Vincent Pelletier',
  author_email='vincent@nexedi.com',
  description="Certificate Authority.",
  long_description=long_description,
  classifiers=[
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Information Technology',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Topic :: Security :: Cryptography',
    'Topic :: System :: Systems Administration :: Authentication/Directory',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
  ],
  keywords='certificate authority',
  url='https://lab.nexedi.com/nexedi/caucase',
  license='GPLv3+ with wide exception for FOSS',
  packages=find_packages(),
  install_requires=[
    'cryptography>=2.2.1', # everything x509 except...
    'pyOpenSSL>=18.0.0', # ...certificate chain validation
    'pem>=17.1.0', # Parse PEM files
    'PyJWT', # CORS token signature
  ],
  zip_safe=True,
  entry_points={
    'console_scripts': [
      'caucase = caucase.cli:main',
      'caucase-probe = caucase.cli:probe',
      'caucase-updater = caucase.cli:updater',
      'caucase-rerequest = caucase.cli:rerequest',
      'caucase-key-id = caucase.cli:key_id',
      'caucased = caucase.http:main',
      'caucased-manage = caucase.http:manage',
    ]
  },
  test_suite='caucase.test',
  use_2to3=True,
)
