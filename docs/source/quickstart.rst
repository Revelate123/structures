Quickstart
==========

Installation
------------

To use Toms-structures, first install it using pip:

.. code-block:: console

   (.venv) $ pip install toms-structures


Overview
--------

The code is organised into two categories, `reinforced_masonry` and `unreinforced_masonry`. 
Within each of these categories, there are various classes representing common masonry types, for example
in `unreinforced_masonry` there is a `Clay()` class, representing commonly found clay fired bricks. 

Once a class is selected e.g. `Clay()`, an object of that type can be created representing a physical 
masonry element. 

Once created, various methods can be applied to the object to determine capacities.