openpyxl-dictreader
===================

Description
-----------

A module that maps the information in each row in an
`openpyxl <https://github.com/chronossc/openpyxl>`__ worksheet to a dict
whose keys are given by the optional fieldnames parameter, similar to
Python's native
`csv.DictReader <https://docs.python.org/3/library/csv.html#csv.DictReader>`__.

Installing
----------

.. code:: python

    pip install openpyxl-dictreader

Examples
--------

Input:

.. code:: python

    import openpyxl_dictreader

    reader = openpyxl_dictreader.DictReader("names.xlsx", worksheet="Sheet1")
    for row in reader:
        print(row["First Name"], row["Last Name"])

Output:

::

    Boris Johnson
    Donald Trump
    Mark Rutte

Acknowledgements
----------------

-  `openpyxl <https://github.com/chronossc/openpyxl>`__
-  `csv <https://docs.python.org/3/library/csv.html#csv.DictReader>`__

