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
"""
Caucase - Certificate Authority for Users, Certificate Authority for SErvices
"""

class CertificateAuthorityException(Exception):
  """Base exception"""
  pass

class NoStorage(CertificateAuthorityException):
  """No space in storage"""
  pass

class NotFound(CertificateAuthorityException):
  """Requested resource does not exist"""
  pass

class Found(CertificateAuthorityException):
  """Resource to create already exists"""
  pass

class CertificateVerificationError(CertificateAuthorityException):
  """Certificate is not valid, it was not signed by CA"""
  pass

class NotACertificateSigningRequest(CertificateAuthorityException):
  """Provided value is not a certificate signing request"""
  pass

class NotJSON(CertificateAuthorityException):
  """Provided value does not decode properly as JSON"""
  pass
