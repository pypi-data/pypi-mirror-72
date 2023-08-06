from os import environ
from pathlib import Path
from sys import platform
from typing import Optional


def install(path: Optional[str] = None):
    '''Search through common locations of SLL certificates on linux and set
    the first existing location to REQUESTS_CA_BUNDLE and HTTPLIB2_CA_CERTS
    environment variables.
    '''
    if platform != 'linux':
        return

    if path is None:
        certs = [
            '/etc/ssl/certs/ca-certificates.crt',  # Debian/Ubuntu/Gentoo etc.
            '/etc/pki/tls/certs/ca-bundle.crt',  # Fedora/RHEL 6
            '/etc/ssl/ca-bundle.pem',  # OpenSUSE
            '/etc/pki/tls/cacert.pem',  # OpenELEC
            '/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem',  # CentOS/RHEL 7
            '/etc/ssl/cert.pem',  # Alpine Linux
        ]

        valid = [cert for cert in certs if Path(cert).is_file()]
        if not valid:
            return

        path = valid[0]

    environ['REQUESTS_CA_BUNDLE'] = environ['HTTPLIB2_CA_CERTS'] = path
