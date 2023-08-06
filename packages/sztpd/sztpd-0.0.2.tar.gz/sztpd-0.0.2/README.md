# Secure Zero Touch Provisioning Daemon (SZTPD)

## Installation

  `pip install sztpd`

## Overview

SZTPD implements the [Bootstrap Server](https://tools.ietf.org/html/rfc8572#section-4.4)
defined in [RFC 8572: Secure Zero Touch Provisioning (SZTP)](https://tools.ietf.org/html/rfc8572).

  * [RESTCONF](https://tools.ietf.org/html/rfc8040)-based interface for programmatic administrative control.
  * Plugins and webhooks enable policy-driven dynamic responses.
  * Single-tenant and multi-tenant deployment modes.
  * A variety of databases backends for flexibility
  * In-memory database supported for ephemeral use-cases (e.g., SDN)

## Usage

```
$ sztpd --help
usage: sztpd [-h] [-v] [-d] [-c CACERT] [-k KEY] database-url

SZTPD implements the "bootstrap server" defined in RFC 8572.

positional arguments:
  database-url          see below for details.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version number and exit.
  -d, --debug           increase debug output level up to 3x (e.g., -ddd)
  -c CACERT, --cacert CACERT
                        path to trust anchor certificates used to authenticate
                        the database (see below for details).
  -k KEY, --key KEY     path to pkcs#12 used to authenticate into the database
                        (see below for details).

Exit status code: 0 on success, non-0 on error.  Error output goes to stderr.

The "cacert" argument is a filepath to a PEM file that contains one or more X.509
certificates.  The list of certificates must be ordered from the certificate of
the issuer to the database's certificate to the self-signed root certificate.

The "key" argument is a filepath to a PEM file that contains a PKCS#12, encoding
both its private key and end-entity certificate.

The "database-url" argument has the form "<dialect>:<dialect-specific-path>".
Three dialects are supported: "sqlite", "postgresql", and "mysql+pymysql".
The dialect-specific-path for each of these is described below.

For the "sqlite" dialect, dialect-specific-path follows the format "///<sqlite-path>",
where sqlite-path can be one of:

  :memory:    - an in-memory database (only useful for testing)
  <filepath>  - an OS-specific filepath to a persisted database file

  Examples:

    $ sztpd sqlite:///:memory:                      (memory)
    $ sztpd sqlite:///relative/path/to/sztpd.db     (unix)
    $ sztpd sqlite:////absolute/path/to/sztpd.db    (unix)
    $ sztpd sqlite:///C:\path\to\sztpd.db           (windows)

For both the "postgresql" and "mysql+pymysql" dialects, the dialect-specific-path
follows the format "//<user>:<passwd>@<host>:<port>/<database-name>".

  Examples:

    The following two examples assume the database is called "sztpd" and
    that the database server listens on the loopback address with no TLS.

      $ sztpd postgresql://user:pass@localhost:5432/sztpd
      $ sztpd mysql+pymysql://user:pass@localhost:3306/sztpd

Please see the documentation for more information.
```


## Documentation

Please see [SZTPD Documentation](https://watsen.net/docs/sztpd).


