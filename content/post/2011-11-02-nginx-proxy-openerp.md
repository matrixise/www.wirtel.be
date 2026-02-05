---
tags:
- devops/server
- devops/virtualization
- python
- python/odoo
date: 2011-11-02
slug: nginx-proxy-openerp
lang: en
title: Nginx and multiple instances of OpenERP

---

## nginx

[Nginx](http://wiki.nginx.org) is a free, open-source, high-performance
HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

## OpenERP

[OpenERP](http://www.openerp.com) is an open source comprehensive suite
of business applications including Sales, CRM, Project management,
Warehouse management, Manufacturing, Accounting and Human Resources.
OpenERP has separate client and server components. XML-RPC interfaces
are available.

In this case study, we will use the XML-RPC protocol because it is based
on the HTTP protocol, which includes the Host header. If you want to use
this configuration for the NetRPC protocol, you will encounter a problem
because this protocol does not include the Host header.

### Install the OpenERP versions

For this setup, I assume you can install both OpenERP v5.0 and v6.0. If
not, you can read my tutorials for the installation of v6.0 or v5.0.

- [Installation of OpenERP
  v5.0](/2011/11/02/install_openerp_v5_on_debian_v6)
- [Installation of OpenERP
  v6.0](/2011/11/02/install_openerp_v6_on_debian_v6)

I will use the installation paths for the rest of my tutorial.

**Don't forget to change the port of your instances.**

For v5.0:

    ~$ ./openerp-server.py --log-level=debug --no-netrpc --port=9069

For v6.0:

    ~$ ./openerp-server.py --log-level=debug --no-netrpc --no-xmlrpcs --xmlrpc-port=10069

### The configuration

In this case study, we know we use the XML-RPC protocol assigned to port
8069.

We will use the proxy module of nginx for the solution. In my example, I
will use the port 9069.

The first openerp will use the port 9069 and the second will be 10069.

For nginx, it's very simple, just define a configuration file for the
servers.

```nginx
server {
    server_name openerp_v5.example.com;
    listen 8069;
    location / {
        proxy_pass http://localhost:9069;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    server_name openerp_v6.example.com;
    listen 8069;

    location / {
        proxy_pass http://localhost:10069;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Don't forget to change your DNS entries to point on the same server, in
this case, localhost:

    127.0.2.1   openerp_v5.example.com openerp_v6.example.com

## Check the configurations

Here is a small python script to check that the proxy is well configured

```python
#!/usr/bin/env python
from xmlrpclib import ServerProxy
def get_version(hostname, port=8069):
    server = ServerProxy('http://%s:%d/xmlrpc/db' % (hostname, port,))
    return server.server_version()

def main():
    print "Version (openerp_v5.example.com): %r" % (get_version('openerp_v5.example.com'),)
    print "Version (openerp_v6.example.com): %r" % (get_version('openerp_v6.example.com'),)

if __name__ == '__main__':
    main()
```