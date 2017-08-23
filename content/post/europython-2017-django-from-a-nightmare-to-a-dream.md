---
title: "EuroPython 2017: Django From A Nightmare To A Dream"
date: 2017-08-16T01:01:56+02:00
draft: true
tags: ["python", "conference", "django", "europython"]
---

# Introduction

With EuroPython 2017, I wanted to contribute to the event, via code.

And of course, the site of [EuroPython](http://europython.org) has been written in [Python](http://www.python.org) with the [Django project](djangoproject.com).

I have found some tips and tricks for the improvement of the site, but I could not work on the main branch of the project because this one is just used by the web site.
And of course, I did not want to break the production site.
So in this case, there was an other solution, firstly, try to add tests and improve the code coverage.

## Why?

Because in the current code of [EuroPython site](https://github.com/EuroPython/epcon), there is no tests, no code coverage and no documentation.

## How to improve the code?

1. Split the configuration
2. Add tests
3. Use the code coverage
4. Use the right tool for the development

### Split the configuration

* `django-dotenv`

Your `.env` file
```python
POSTGRES_USER="postgres"
POSTGRES_PASSWORD=""

SECRET_KEY="whoami"
ALLOWED_HOSTS=''
CSRF_COOKIE_SECURE=False
DEBUG=True
ENVIRONMENT='LOCAL'

DJANGO_SETTINGS_MODULE=dev-settings
```

Your `manage.py` file

```python
import dotenv
if __name__ == '__main__':
    dotenv.read_dotenv()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    ...
```


### Add tests

Firstly, as you know, the default test runner in `Django`, is `unittest` but `pytest` is a better solution and the first step is just to install it.

And why we need to change from `unittest` to `pytest` ?

1. `pytest` is compatible with `unittest`
2. `pytest-django` adds some parameters, for example, `--nomigrations`. This flag on the command `pytest` will not execute the migrations when we execute the tests.

With the version 1.7, `Django` introduced a migration engine but this engine is executed when we run the tests. The main problem with this behaviour, the tests will take more time for the execution. With the `--nomigrations` flag, the migrations are not executed and the tests are just too quick.

```shell
pip install pytest
pip install pytest-django
pip install django-test-without-migrations
```

`pytest` has a configuration file `pytest.ini` and here is the content.

```ini
[pytest]
addopts = --nomigrations
```

So, how to add some tests ? for the models, maybe with the `factory_boy` library and because the site is running with `python2`, we have to install the `mock` library.

```shell
pip install factory_boy
pip install -e git+https://github.com/FactoryBoy/django-factory_boy#egg=master
pip install mock
```

Here is an example with Factory Boy

```python
from django.template.defaultfilters import slugify

import factory
import factory.django
from faker import Faker
from django_factory_boy import auth as auth_factories

from conference.models import (TALK_LEVEL, TALK_STATUS, TALK_LANGUAGES)
from conference.models import Conference

fake = Faker()

def default_talk_title(talk):
    return fake.sentence(nb_words=6, variable_nb_words=True)[:80]

def default_talk_slug(talk):
    return slugify(talk.title)

class TalkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'conference.Talk'

    title = factory.LazyAttribute(default_talk_title)
    sub_title = factory.Faker('sentence', nb_words=6, variable_nb_words=True)

    duration = 30

    slug = factory.LazyAttribute(default_talk_slug)
    level = factory.Iterator(TALK_LEVEL, getter=lambda x: x[0])
    status = factory.Iterator(TALK_STATUS, getter=lambda x: x[0])
    conference = factory.Iterator(Conference.objects.all().values_list('code', flat=True))

    language = factory.Iterator(TALK_LANGUAGES, getter=lambda x: x[0])
```

If we want to mock the send of an email, we can do that

```python
from unittest import mock
from django.test import TestCase

class TestEmail(TestCase):
    @mock.patch('django.core.mail.send_mail')
    def test_mail(self, mock_send_mail):
        # in this method, you can write your test
```

### Code Coverage

The code coverage is not a perfect metric but I think it can be really useful because we can learn the code and start to write the right test for the coverage of a part of the code.

```shell
pip install coverage
pip install pytest-cov
pip install django-coverage-plugin
```

![Debug Toolbar](/europython-2017-django-from-a-nightmare-to-a-dream/screenshot-coverage-html.png)


### Write Code/Refactoring

* `pyflake8`
* `pylint`
* `vulture`
* `isort`
* `autoflake`
* `mypy`


`mypy` with `mypy-django`
```
gnrbag.py:84: error: Incompatible types in assignment (expression has type "classmethod", variable has type Callable[[Any], Any])
gnrbag.py:317: error: Name 'json' already defined
gnrbag.py:2874: error: Need type annotation for variable
gnrbag.py:3083: error: Dict entry 3 has incompatible type "str": "str"
```


### Documentation

It's my humble opinion, the best tool is Sphinx because we can use the Restructured Text and of course, we can extend the parser with directives and roles.

```shell
pip install sphinx
```

### Profiling

```shell
pip install django-devserver
pip install line_profiler
pip install cprofilev
pip install pytest-profiling
pip install django-debug-toolbar
```

![Debug Toolbar](/europython-2017-django-from-a-nightmare-to-a-dream/django-debug-toolbar.png)

```
[11/Jul/2017 12:26:50] "GET /favicon.ico HTTP/1.1" 302 0
[11/Jul/2017 12:26:50] "GET /en/favicon.ico HTTP/1.1" 301 0
    [sql] (3ms) 1 queries with 0 duplicates
    [profile] Total time to render was 0.03s
    [profile] Timer unit: 1e-06 s

	Total time: 0.009523 s
	File: /home/stephane/.virtualenvs/ep2017/lib/python2.7/site-packages/cms/views.py
	Function: details at line 23

	Line #      Hits         Time  Per Hit   % Time  Line Contents
	==============================================================
	23  def details(request, slug):
	24    """
	25    The main view of the Django-CMS! Takes a request and a slug, renders the
	26    page.
	27    """

```

`pytest-profiling` uses `cProfile` and can generate a `.prof` file.

```
$ pytest --durations=2 --profile-svg
======================== slowest 2 test durations ============================================
0.47s setup    assopy/tests/test_reset_password.py::ResetPasswordTestCase::test_reset_password
0.36s call     assopy/tests/test_stripe.py::StripeViewTestCase::test_add_stripe_on_order_test
```

`cprofilev` is a web interface for the `cProfile` file.

```
cprofilev -f prof/test_reset_password.prof
[cProfileV]: cProfile output available at http://127.0.0.1:4000
```

![cProfile](/europython-2017-django-from-a-nightmare-to-a-dream/screenshot-cprofile.png)

# Result

* Sprint Code
* Tests
* Code coverage
* Port to PostgreSQL
* Port to Python 3.6
