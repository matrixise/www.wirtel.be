---
author: Stephane Wirtel
date: 2012-02-04
lang: en
slug: postgresql-foreign-data-wrapper-openerp
tags:
- python
- openerp
- postgresql
- fdw
title: PostgreSQL - Foreign Data Wrapper

---

# PostgreSQL - Foreign Data Wrapper for OpenERP

Here is a simple example, but via this connector we can connect to
#OpenERP from PostgreSQL

```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# copyright: 2012 - Stephane Wirtel <stw@openerp.com>
from multicorn import ForeignDataWrapper
from .utils import log_to_postgres
from itertools import cycle
from datetime import datetime

from rpc import XmlRPCConnector, Connection, Object

class OpenERPForeignDataWrapper(ForeignDataWrapper):
    def __init__(self, fdw_options, fdw_columns):
        super(OpenERPForeignDataWrapper, self).__init__(fdw_options, fdw_columns)
        self.connector = XmlRPCConnector(fdw_options['hostname'],
                                                 int(fdw_options['port']))
        self.cnx = Connection(self.connector,
                              fdw_options['database'],
                              fdw_options['username'],
                              fdw_options['password'])
        self.object_name = fdw_options['object']

    def execute(self, quals, columns):
        log_to_postgres(str(quals))
        log_to_postgres(str(columns))

        proxy = Object(self.cnx, self.object_name)

        item = {}
        for record in proxy.select([], fields=list(columns)):
            for column in columns:
                item[column] = record[column]
            yield item
```

## multicorn

I just created a small shell script to drop and create the database, and
create the server.

```sql
#!/usr/bin/env bash

PGSQL=/usr/bin/psql

DATABASE=openerp_multicorn

$PGSQL -d postgres -c "DROP DATABASE IF EXISTS ${DATABASE}"
createdb $DATABASE
$PGSQL -d $DATABASE <<-EOF
CREATE EXTENSION multicorn;

CREATE SERVER multicorn_openerp 
    FOREIGN DATA WRAPPER multicorn 
    OPTIONS (wrapper 'multicorn.openerpfdw.OpenERPForeignDataWrapper');

CREATE FOREIGN TABLE external_oe_users (
    login character varying,
    name character varying)
    SERVER multicorn_openerp OPTIONS (
        hostname 'localhost',
        port '8069',
        database 'openerp',
        username 'admin',
        password 'admin',
        object 'res.users'
    );

SELECT login, name FROM external_oe_users where login='admin';

EOF
```

```text
stephane@atlantis:~$ ./multicorn.sh 
DROP DATABASE
CREATE EXTENSION
CREATE SERVER
CREATE FOREIGN TABLE
NOTICE:  [login = admin]
NOTICE:  set(['login', 'name'])
 login | name  
-------+-------
 admin | Admin
(1 row)
```