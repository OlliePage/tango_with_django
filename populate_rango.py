"""
Entering test data into your database tends to be a hassle. Many developers will
add in some bogus test data by randomly hitting keys, like wTFzmN00bz7. Rather
than do this, it is better to write a script to automatically populate the database
with realistic and credible data. This is because when you go to demo or test your
app, you’ll need to be able to see some credible examples in the database. If you’re
working in a team, an automated script will mean each collaborator can simply run
that script to initialise the database on their computer with the same sample data
as you. It’s therefore good practice to create what we call a population script.
To create a population script, create a new file called populate_rango.py. Create
this file in <workspace>/tango_with_django_project/, or in other words, your Django
project’s root directory. When the file has been created, add the following code.

Single use script using Django Models to populate database
While creating a population script may take time initially, you will save yourself
heaps of time in the long run. When deploying your app elsewhere, running the
population script after setting everything up means you can start demonstrating
your app straight away. You’ll also find it very handy when it comes to unit testing
your code.
"""

import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
import django

django.setup()

from rango.models import Page, Category


def populate():
    """
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.
    :return:
    """

    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/',
         'views': random.randint(10, 100)},
        {'title': 'How to Think Like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/',
         'views': random.randint(10, 100)},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/',
         'views': random.randint(10, 100)}]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': random.randint(10, 100)},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/',
         'views': random.randint(10, 100)},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/',
         'views': random.randint(10, 100)}]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/',
         'views': random.randint(10, 100)},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org',
         'views': random.randint(10, 100)}]

    cats = {'Python': dict(pages=python_pages, views=128, likes=64),
            'Django': dict(pages=django_pages, views=64, likes=32),
            'Other Frameworks': dict(pages=other_pages, views=32, likes=16)}

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, likes, views):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.views = views
    c.save()
    return c


if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
