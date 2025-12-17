Quickstart
========

Installation
------------

To use Toms-structures, first install it using pip:

.. code-block:: console

   (.venv) $ pip install toms-structures


Usage
-----

The code is currently organised into two categories, ``reinforced_masonry`` and ``unreinforced_masonry``, largely representing 
sections 7 for unreinforced masonry and section 8 for reinforced masonry from AS3700:2018.

Within each of these categories, there are classes representing common masonry types, for example
in ``unreinforced_masonry`` there is a ``Clay()`` class, representing commonly found clay fired bricks. These classes largely only 
serve to apply default values specific to the type of masonry. For example, the calculation of km (Cl 3.3.2) varies with masonry type.
It is the eventual goal that all common types of masonry will have their own classes.

Once a class is selected e.g. ``Clay()``, an object of that type can be created representing a physical 
masonry element. For example:

.. code-block:: python

   from toms_structures.unreinforced_masonry import Clay
   wall = Clay(fuc=20,length=1000,thickness=110,height=3000,bedding_type=True,mortar_class=3)

Once created, various methods can be applied to the object to determine capacities. Check out the :doc:`examples <examples>` page for more information
