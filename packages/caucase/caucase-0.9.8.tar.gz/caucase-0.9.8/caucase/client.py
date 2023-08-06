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
from __future__ import absolute_import
import datetime
import httplib
import json
import os
import ssl
from urlparse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions
from . import utils
from . import version

__all__ = (
  'CaucaseError',
  'CaucaseClient',
  'HTTPSOnlyCaucaseClient',
)

_cryptography_backend = default_backend()

class CaucaseError(Exception):
  """
  Raised when server responds with an HTTP error status.
  """
  pass

class CaucaseClient(object):
  """
  Caucase HTTP(S) client.

  Expose caucase REST API as pythonic methods.
  """
  HTTPConnection = httplib.HTTPConnection
  HTTPSConnection = httplib.HTTPSConnection

  @classmethod
  def updateCAFile(cls, url, ca_crt_path):
    """
    Bootstrap and maintain a CA file up-to-date.

    url (str)
      URL to caucase, ending in eithr /cas or /cau.
    ca_crt_path (str)
      Path to the CA certificate file or directory, which may not exist.
      If it does not exist, it is created. If there is an extension, a file is
      created, otherwise a directory is.

    Return whether an update happened (including whether an already-known
    certificate expired and was discarded).
    """
    loaded_ca_pem_list = utils.getCertList(ca_crt_path)
    if not loaded_ca_pem_list:
      ca_pem = cls(ca_url=url).getCACertificate()
      utils.saveCertList(ca_crt_path, [ca_pem])
      updated = True
      # Note: reloading from file instead of using ca_pem, to exercise the
      # same code path as future executions, to apply the same checks.
      loaded_ca_pem_list = utils.getCertList(ca_crt_path)
    else:
      updated = False
    now = datetime.datetime.utcnow()
    ca_pem_list = [
      x
      for x in loaded_ca_pem_list
      if utils.load_ca_certificate(x).not_valid_after > now
    ]
    ca_pem_list.extend(
      cls(ca_url=url, ca_crt_pem_list=ca_pem_list).getCACertificateChain(),
    )
    if ca_pem_list != loaded_ca_pem_list:
      utils.saveCertList(ca_crt_path, ca_pem_list)
      updated = True
    return updated

  @classmethod
  def updateCRLFile(cls, url, crl_path, ca_list):
    """
    Bootstrap anf maintain a CRL file up-to-date.

    url (str)
      URL to caucase, ending in eithr /cas or /cau.
    crl_path (str)
      Path to the CRL file, which may not exist.
    ca_list (list of cryptography.x509.Certificate instances)
      One of these CA certificates must have signed the CRL for it to be
      accepted.

    Return whether an update happened.
    """
    if os.path.exists(crl_path):
      with open(crl_path, 'rb') as crl_file:
        my_crl = utils.load_crl(crl_file.read(), ca_list)
    else:
      my_crl = None
    latest_crl_pem = cls(ca_url=url).getCertificateRevocationList()
    latest_crl = utils.load_crl(latest_crl_pem, ca_list)
    if my_crl is None or latest_crl.signature != my_crl.signature:
      with open(crl_path, 'wb') as crl_file:
        crl_file.write(latest_crl_pem)
      return True
    return False

  def __init__(
    self,
    ca_url,
    ca_crt_pem_list=None,
    user_key=None,
    http_ca_crt_pem_list=None,
  ):
    # XXX: set timeout to HTTP connections ?
    http_url = urlparse(ca_url)
    port = http_url.port or 80
    self._http_connection = self.HTTPConnection(
      http_url.hostname,
      port,
      #timeout=,
    )
    self._ca_crt_pem_list = ca_crt_pem_list
    self._path = http_url.path
    ssl_context = ssl.create_default_context(
      # unicode object needed as we use PEM, otherwise create_default_context
      # expects DER.
      cadata=(
        utils.toUnicode(''.join(http_ca_crt_pem_list))
        if http_ca_crt_pem_list
        else None
      ),
    )
    if http_ca_crt_pem_list: # pragma: no cover
      pass
    else:
      ssl_context.check_hostname = False
      ssl_context.verify_mode = ssl.CERT_NONE
    if user_key:
      try:
        ssl_context.load_cert_chain(user_key)
      except ssl.SSLError as exc:
        raise ValueError('Failed to load user key: %r' % (exc, ))
    self._https_connection = self.HTTPSConnection(
      http_url.hostname,
      443 if port == 80 else port + 1,
      #timeout=,
      context=ssl_context,
    )

  def _request(self, connection, method, url, body=None, headers=None):
    path = self._path + url
    headers = headers or {}
    headers.setdefault('User-Agent', 'caucase ' + version.__version__)
    connection.request(method, path, body, headers)
    response = connection.getresponse()
    response_body = response.read()
    if response.status >= 400:
      raise CaucaseError(response.status, response.getheaders(), response_body)
    assert response.status < 300 # caucase does not redirect
    if response.status == 201:
      return response.getheader('Location')
    return response_body

  def _http(self, method, url, body=None, headers=None):
    return self._request(self._http_connection, method, url, body, headers)

  def _https(self, method, url, body=None, headers=None):
    return self._request(self._https_connection, method, url, body, headers)

  def getCertificateRevocationList(self):
    """
    [ANONYMOUS] Retrieve latest CRL.
    """
    return self._http('GET', '/crl')

  def getCertificateSigningRequest(self, csr_id):
    """
    [ANONYMOUS] Retrieve an CSR by its identifier.
    """
    return self._http('GET', '/csr/%i' % (csr_id, ))

  def getPendingCertificateRequestList(self):
    """
    [AUTHENTICATED] Retrieve all pending CSRs.
    """
    return json.loads(self._https('GET', '/csr').decode('utf-8'))

  def createCertificateSigningRequest(self, csr):
    """
    [ANONYMOUS] Store a CSR and return its identifier.
    """
    return int(self._http('PUT', '/csr', csr, {
      'Content-Type': 'application/pkcs10',
    }))

  def deletePendingCertificateRequest(self, csr_id):
    """
    [AUTHENTICATED] Reject a pending CSR.
    """
    self._https('DELETE', '/csr/%i' % (csr_id, ))

  def _getCertificate(self, crt_id):
    return self._http('GET', '/crt' + crt_id)

  def getCertificate(self, csr_id):
    """
    [ANONYMOUS] Retrieve CRT by its identifier (same as corresponding CRL
    identifier).
    """
    return self._getCertificate('/%i' % (csr_id, ))

  def getCACertificate(self):
    """
    [ANONYMOUS] Retrieve current CA certificate.
    """
    return self._getCertificate('/ca.crt.pem')

  def getCACertificateChain(self):
    """
    [ANONYMOUS] Retrieve CA certificate chain, with CA certificate N+1 signed
    by CA certificate N, allowing automated CA cert rollout.
    """
    found = False
    previous_ca = trust_anchor = sorted(
      (
        utils.load_ca_certificate(x)
        for x in self._ca_crt_pem_list
      ),
      key=lambda x: x.not_valid_before,
    )[-1]
    result = []
    for entry in json.loads(
      self._getCertificate('/ca.crt.json').decode('utf-8'),
    ):
      try:
        payload = utils.unwrap(
          entry,
          lambda x: x['old_pem'],
          utils.DEFAULT_DIGEST_LIST,
        )
      except cryptography.exceptions.InvalidSignature:
        continue
      if not found:
        found = utils.load_ca_certificate(
          utils.toBytes(payload['old_pem']),
        ) == trust_anchor
      if found:
        if utils.load_ca_certificate(
          utils.toBytes(payload['old_pem']),
        ) != previous_ca:
          raise ValueError('CA signature chain broken')
        new_pem = utils.toBytes(payload['new_pem'])
        result.append(new_pem)
        previous_ca = utils.load_ca_certificate(new_pem)
    return result

  def renewCertificate(self, old_crt, old_key, key_len):
    """
    [ANONYMOUS] Request certificate renewal.
    """
    new_key = utils.generatePrivateKey(key_len=key_len)
    return (
      utils.dump_privatekey(new_key),
      self._http(
        'PUT',
        '/crt/renew',
        json.dumps(
          utils.wrap(
            {
              'crt_pem': utils.toUnicode(utils.dump_certificate(old_crt)),
              'renew_csr_pem': utils.toUnicode(utils.dump_certificate_request(
                x509.CertificateSigningRequestBuilder(
                ).subject_name(
                  # Note: caucase server ignores this, but cryptography
                  # requires CSRs to have a subject.
                  old_crt.subject,
                ).sign(
                  private_key=new_key,
                  algorithm=utils.DEFAULT_DIGEST_CLASS(),
                  backend=_cryptography_backend,
                ),
              )),
            },
            old_key,
            utils.DEFAULT_DIGEST,
          ),
        ).encode('utf-8'),
        {'Content-Type': 'application/json'},
      ),
    )

  def revokeCertificate(self, crt, key=None):
    """
    Revoke certificate.
    [ANONYMOUS] if key is provided.
    [AUTHENTICATED] if key is missing.
    """
    crt = utils.toUnicode(crt)
    if key:
      method = self._http
      data = utils.wrap(
        {
          'revoke_crt_pem': crt,
        },
        utils.load_privatekey(key),
        utils.DEFAULT_DIGEST,
      )
    else:
      method = self._https
      data = utils.nullWrap({
        'revoke_crt_pem': crt,
      })
    method(
      'PUT',
      '/crt/revoke',
      json.dumps(data).encode('utf-8'),
      {'Content-Type': 'application/json'},
    )

  def revokeSerial(self, serial):
    """
    Revoke certificate by serial.

    This method is dangerous ! Prefer revokeCRT whenever possible.

    [AUTHENTICATED]
    """
    self._https(
      'PUT',
      '/crt/revoke',
      json.dumps(utils.nullWrap({'revoke_serial': serial})).encode('utf-8'),
      {'Content-Type': 'application/json'},
    )

  def createCertificate(self, csr_id, template_csr=''):
    """
    [AUTHENTICATED] Sign certificate signing request.
    """
    header_dict = {}
    if template_csr:
      header_dict['Content-Type'] = 'application/pkcs10'
    self._https('PUT', '/crt/%i' % (csr_id, ), template_csr, header_dict)

class HTTPSOnlyCaucaseClient(CaucaseClient):
  """
  Like CaucaseClient, but forces anonymous accesses to go through HTTPS as
  well.
  """
  def __init__(self, *args, **kw):
    super(HTTPSOnlyCaucaseClient, self).__init__(*args, **kw)
    self._http_connection = self._https_connection
