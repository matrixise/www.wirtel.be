+++
title = "Connect to Odoo in your application with ERPpeek"
tags = ["python", "openerp", "odoo", "erppeek", "xmlrpc"]
date = "2014-06-13T18:16:29+01:00"
categories = ["programming"]
image = "background.jpg"
# aliases = [
#    "/posts/en/2014/06/13/using_erppeek_to_discuss_with_openerp"
#]
+++

In this post, we will use the new name, [Odoo] instead of [OpenERP] but
the content and the examples are compatible with OpenERP 5.0, 6.0, 6.1 and 7.0
and of course with Odoo v8.0. There is no need to be worried, I will try to be
compatible with the new version.

If you are glad with this content, just inform me via [my twitter account](https://twitter.com/matrixise).

Usually, when you want to discuss with [Odoo] in Python, you have several
options.

1. Based on the [HTTP protocol](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol), you have the [xmlrpc] and [jsonrpc] protocols.
2. Based on the simple socket, you can use the **netrpc** (there is no documentation for this protocol).

### The protocols

1. xmlrpc (since the beginning of Odoo)
   
   * available from the first version of OpenERP
   * based on HTTP (allow the virtual hosting with a reverse-proxy [nginx])
   * very simple
   * available in the standard library of Python via the [xmlrpclib] module

2. jsonrpc (introduced in OpenERP 7.0)

   * introduced in OpenERP 7.0 via the web module
   * based on HTTP (virtualhost via [nginx])
   * need a web session

3. netrpc (deprecated)

   * available for some versions of OpenERP
   * use socket and the Pickle module of Python

Imagining that you want to show the users from the database, you can use the
following code with the [xmlrpclib] module of the Standard Library of Python.

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
from xmlrpclib import ServerProxy

SERVER = 'http://localhost:8069'
DATABASE = 'demo'
USERNAME = 'admin'
PASSWORD = 'admin'

server = ServerProxy('http://localhost:8069/xmlrpc/common')
user_id = server.login(DATABASE, USERNAME, PASSWORD)

server = ServerProxy('http://localhost:8069/xmlrpc/object')
user_ids = server.execute(
    DATABASE, user_id, PASSWORD,
    'res.users', 'search', []
)

users = server.execute(
    DATABASE, user_id, PASSWORD,
    'res.users', 'read', user_ids, []
)

for user in users:
    print(user['id'], user['name'])

{{< /highlight >}}

With the above example, I think it's not very verbose, the code is very simple.
We use the ServerProxy object from the [xmlrpclib] library and the library does
the rest.

But in some cases, for example, if you have a lot of xmlrpc calls, the code
starts to be too long and very verbose. And by the way, I think you will not
like write a file with one hundred of lines.

Now, we will use the [ERPpeek] library by :github:`Florent Xicluna <florentx>`.

Here is the same example with ERPpeek

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

SERVER = 'http://localhost:8069'
DATABASE = 'demo'
USERNAME = 'admin'
PASSWORD = 'admin'

client = erppeek.Client(SERVER, DATABASE, USERNAME, PASSWORD)

proxy = client.model('res.users')
# No need to use the model.search method, the model.browse method accepts a domain
users = proxy.browse([])

for user in users:
    print("{user.id} {user.name}".format(user=user))
{{< /highlight >}}


Interested in this library? Let's go for this tutorial.

Firstly, you need to install the library. In my case, I prefer to use a
[virtualenv] but you are free to do as you want. The installation will be
executed via the [pip] command (from the python-pip package if you are using
debian or ubuntu).

In the case where you want to use a virtualenv.

{{< highlight bash >}}
pip install virtualenv
virtualenv ~/.venvs/erppeek
source ~/.venvs/erppeek/bin/activate
{{< /highlight >}}

Once your environment is installed, you can install the library with [pip].

# Install the library

{{< highlight bash >}}
pip install erppeek
{{< /highlight >}}

After that, you'll be free to use it via the CLI provided by the library,
because this one contains a CLI called erppeek ;-) Or you can use the library
via the API and in this tutorial, we will use this option, the API.

# List the databases

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

SERVER = 'http://localhost:8069'

client = erppeek.Client(server=SERVER)

for database in client.db.list():
   print('database: %r' % (database,))
{{< /highlight >}}

# Check if a database exists

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

DATABASE = 'demo'
SERVER = 'http://localhost:8069'

client = erppeek.Client(server=SERVER)

database_exists = DATABASE in client.db.list()

if database_exists:
    print("Database {} exists".format(DATABASE))
else:
    print("Database {} does not exist".format(DATABASE))
{{< /highlight >}}

# Create a database

Firstly, when you start with [Odoo], you want to create a new database.

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

DATABASE = 'demo'
SERVER = 'http://localhost:8069'
ADMIN_PASSWORD = 'admin'

client = erppeek.Client(server=SERVER)

if not DATABASE in client.db.list():
    print("the database does not exist...")
    client.create_database(ADMIN_PASSWORD, DATABASE)
{{< /highlight >}}

# Default configuration

erppeek allows you to use a .INI file (**erppeek.ini**) for the configuration of
several environments. By the way, instead of using the **erppeek.Client** method,
and pass the arguments for the connection, you can use the
**erppeek.Client.from_config** method and give the right environment.

{{< highlight ini >}}
[demo]
host = localhost
port = 8069
database = demo
username = admin
password = admin
{{< /highlight >}}

For example, here is the right code

{{< highlight python >}}
#!/usr/bin/env python
import erppeek

# if you don't use the configuration file, you need to use the __init__
# method of the Client class
client = erppeek.Client('http://localhost:8069', 'demo', 'admin', 'admin')

# you can use the erppeek.Client.from_config method

client = erppeek.Client.from_config('demo')
{{< /highlight >}}

# List the installed modules

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

client = erppeek.Client.from_config('demo')
installed_modules = client.modules(installed=True)

for module in installed_modules['installed']:
    print(module)

# or you can use the other code which use the model('ir.module.module')

proxy = client.model('ir.module.module')
installed_modules = proxy.browse([('state', '=', 'installed')])

for module in installed_modules:
    print('{:>5} {}'.format(module.name, module.description))
{{< /highlight >}}

# Update the module list

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

client = erppeek.Client.from_config('demo')
proxy = client.model('ir.module.module')
proxy.update_list()
{{< /highlight >}}

# Install the CRM module

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

client = erppeek.Client.from_config('demo')
modules = client.modules('crm', installed=False)
if 'crm' in modules['uninstalled']:
    client.install('crm')
{{< /highlight >}}

# List the models

Here is a part of code which shows how to fetch the list of the models installed
in the database.

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

client = erppeek.Client.from_config('demo')
proxy = client.model('ir.model')
for model in proxy.browse([]):
    print("{model.model} {model.state}".format(model=model))
{{< /highlight >}}

# Show the description of a model

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

DEFAULTS = dict(help='', string='Unknown')

client = erppeek.Client.from_config('demo')
user_model = client.model('res.users')

for fname, field in sorted(user_model.fields().items()):
    values = dict(DEFAULTS, name=fname, **field)

print("{name:30} {type:10} {string}".format(**values))
{{< /highlight >}}

# Create a new model

In this example, we will see how to create a new model via XML-RPC and add a new
field.

{{< highlight python >}}
#!/usr/bin/env python
from __future__ import print_function
import erppeek

client = erppeek.Client.from_config('demo')
model_proxy = client.model('ir.model')
field_proxy = client.model('ir.model.fields')

values = {
    'model': 'x_contact',
    'name': 'Contact',
    'state': 'manual',
}

# With this instruction, you are going to create the model
# in the database without one line of python code.
model = model_proxy.create(values)

values = {
    'name': 'x_firstname',
    'ttype': 'char',
    'size': 64,
    'field_description': 'Firstname',
    'model_id': model.id,
    'model': model.model,
    'domain': '[]',
}
field = field_proxy.create(values)
{{< /highlight >}}

With this code, you will be able to create a new record with ERPpeek

{{< highlight python >}}
contact_proxy = client.model('x_contact')
contact_proxy.create({'x_firstname': 'Stephane'})

for contact in contact_proxy.browse([]):
    print(contact.x_firstname)
{{< /highlight >}}


In the second part of this series, I will explain how to create an invoice and
print it with the old system (RML) and the new system (Webkit) and a lot of
funny stuff ;-)

You can send me your feedback and I will adapt my post with your experience of
Erppeek.



# Troubleshooting

## Connection refused

In this case, just check that your server is running ;-)

[erppeek]: http://github.com/florentx/erppeek
[jsonrpc]: http://en.wikipedia.org/wiki/JSON-RPC
[Odoo]: http://odoo.com
[OpenERP]: http://openerp.com
[pip]: https://pip.pypa.io/en/latest/
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/
[xmlrpc]: http://en.wikipedia.org/wiki/XML-RPC
[xmlrpclib]: https://docs.python.org/2/library/xmlrpclib.html
[nginx]: http://nginx.org
