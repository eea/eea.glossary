***************
Glossary
***************

.. contents:: Table of Contents

Import data from JSON
=====================

An upgrade step can be used to import the data from the old EEA Glossaries
into three instances of the eea.glossary: EEA Glossary, EPER and EPER2.

Import procedure
----------------

#. Install content type
#. In the ZMI interface open portal_setup, "Upgrades" tab, select
   eea.glossary:default and click "Choose Profile"
#. Click "Show" to show the old upgrades
#. Select the step "Import terms and synonyms from json (1.0 --> 1.0)"
   and click Upgrade

Life, the Universe, and Everything
==================================

A Dexterity-based content type to define a glossary and its terms.

This package is inspired in `PloneGlossary`_ and `collective.glossary`_.

.. _`PloneGlossary`: https://pypi.python.org/pypi/Products.PloneGlossary
.. _`collective.glossary`: https://pypi.python.org/pypi/collective.glossary

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        eea.glossary

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``eea.glossary`` and click the 'Activate' button.


Screenshots
-----------

.. figure:: https://raw.github.com/eea/eea.glossary/master/docs/glossary.png
    :align: center
    :height: 640px
    :width: 768px

    Create a Glossary.

.. figure:: https://raw.github.com/eea/eea.glossary/master/docs/usage.png
    :align: center
    :height: 640px
    :width: 768px

    Use it!

.. figure:: https://raw.github.com/eea/eea.glossary/master/docs/controlpanel.png
    :align: center
    :height: 400px
    :width: 768px

    The tooltip can be disabled in the control panel configlet.

Developer Notes
---------------

The terms are loaded in a page using an AJAX call to a browser view that returns them as a JSON object.

The tooltips will only be available in the default view of a content type instance.
