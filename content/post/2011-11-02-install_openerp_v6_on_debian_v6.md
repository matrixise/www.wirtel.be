---
tags:
- python/odoo
date: 2011-11-02
slug: install_openerp_v6_on_debian_v6
title: Installation of OpenERP 6.0 on Debian 6.0

---

# How to install OpenERP 6.0 on Debian 6.0

## OpenERP

OpenERP is an open source comprehensive suite of business applications
including Sales, CRM, Project management, Warehouse management,
Manufacturing, Accounting and Human Resources. OpenERP has separate
client and server components. XML-RPC interfaces are available.

In this case study, we will use the XML-RPC protocol because it is
based on the HTTP protocol, which includes the Host header. If you want
to use this configuration for the NetRPC protocol, you will encounter a
problem because this protocol does not include the Host header.

- [OpenERP](http://www.openerp.com)

### Install the dependencies

With your root access, we will install the dependencies for OpenERP
v6.0.

```bash
~# useradd -m -s /bin/bash openerp 
~# apt-get install postgresql
~# su postgres -c "createuser -s openerp"
~# apt-get install python-psycopg2 python-reportlab python-voject
~# apt-get install python-lxml python-pychart python-tz
~# apt-get install python-yaml python-mako
```

### Fetch and Execute OpenERP

Using the openerp user:

```bash
~$ mkdir openerp
```

```bash
~$ wget http://www.openerp.com/download/stable/source/openerp-server-6.0.3.tar.gz
~$ tar xfz openerp-server-6.0.3
~$ cd openerp-server-6.0.3/server/bin
~$ ./openerp-server.py --log-level=debug
```

### Connect to the server

- You can use the GTK client and set the appropriate information in the
  connection dialog box
- You can use this Python code

```python
#!/usr/bin/env python
from xmlrpclib import ServerProxy
def get_version(hostname, port=8069):
    server = ServerProxy('http://%s:%d/xmlrpc/db' % (hostname, port,))
    return server.server_version()

def main():
    print "Version: %r" % (get_version('localhost'),)

if __name__ == '__main__':
    main()
```