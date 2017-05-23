pymultigen - Multi-file frontend for single-file code generators
================================================================

.. image:: https://travis-ci.org/moltob/pymultigen.svg?branch=master
    :target: https://travis-ci.org/moltob/pymultigen

.. image:: https://badge.fury.io/py/pymultigen.svg
    :target: https://badge.fury.io/py/pymultigen

This small library adds multi-file management on top of one or more existing single-file code
generators.

Why would I need pymultigen?
----------------------------

Code generators like Mako or Jinja are great and can be used to generate just about any kind of
textual output from templates with a nice template language. They are very mature and battle-proven.
However, most of those generators have their origin in the web application domain. The typical
usecase is to dynamically render a single HTTP response (most of the time an HTML page) from one or
more templates. *One* HTML page.

If you want to use these generators in other scenarious, e.g. to generate code or reports, but not
to *one* but to *multiple* files in different folders, pymultigen can help. It simply adds an easy
to configure file and folder management layer on top of one or more existing code generators.

More docs to come soon.
