Data inventory tool
###################

With this tool you can inspect various data sources and generate data
inventory tables. Data inventory table essentially contains list of tables
and table columns of a specified data source.

Inventory tables are designed to be easily readable and editable using a
spreadsheet program.

Here is an example how you can generate inventory table from a CSV file::

    inventory-table inspect cvs data.cvs


How to install
==============

In order to install this tool, first you need to install Python_. When you
have Python installed, then install data inventory tool like this::

    pip install data-inventory-tool

.. _Python: https://www.python.org/downloads/


Generating inventory table
==========================

PostgreSQL
----------

For PostgreSQL first you need to install PostgreSQL driver::

    pip install psycopg2-binary

Then generate inventory table like this::

    inventory-table inspect sql postgresql://user:password@host:port/db

MySQL
-----

For MySQL first you need to install MySQL driver::

    pip install mysqlclient

Then generate inventory table like this::

    inventory-table inspect sql mysql+mysqldb://user:password@host:port/db


Troubleshooting
===============

If you get errors like this::

    Error: Database driver not found: No module named 'psycopg2'.
    See: https://docs.sqlalchemy.org/en/13/dialects/index.html

That means, you don't have a required database driver installed.
