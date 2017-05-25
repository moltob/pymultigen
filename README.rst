pymultigen - Multi-file frontend for single-file code generators
================================================================

.. image:: https://travis-ci.org/moltob/pymultigen.svg?branch=master
    :target: https://travis-ci.org/moltob/pymultigen

.. image:: https://badge.fury.io/py/pymultigen.svg
    :target: https://badge.fury.io/py/pymultigen

.. image:: https://coveralls.io/repos/github/moltob/pymultigen/badge.svg?branch=master
    :target: https://coveralls.io/github/moltob/pymultigen?branch=master

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg

This small library adds multi-file management on top of one or more existing single-file code
generators.

.. contents:: :depth: 2

Why would I need pymultigen?
----------------------------

Code generators like `Mako <http://www.makotemplates.org/>`_ or `Jinja <http://jinja.pocoo.org/>`_
are great and can be used to generate just about any kind of textual output from templates with a
nice template language. They are very mature and battle-proven. However, most of those generators
have their origin in the web application domain. The typical usecase is to dynamically render a
single HTTP response (most of the time an HTML page) from one or more templates. *One* HTML page.

If you want to use these generators in other scenarious, e.g. to generate code or reports, but not
to *one* but to *multiple* files in different folders, pymultigen can help. It simply adds an easy
to configure file and folder management layer on top of one or more existing code generators.

Installation
------------

pymultigen comes in form or a regular Python distribution and can be installed from Github or PyPI
with a simple:

.. code-block:: shell

    $ pip install pymultigen

The library works with any version of Python >= 3.3.

Usage
-----

The overall concept of pymultigen is simple:

* A ``Generator`` class controls the overall generation workflow. The most important method it
  implements is ``generate(model, folder)``. This is the single method called by *users* of the
  created multi-file generator.
* The ``Generator`` has a static list of ``Task`` objects. Each ``Task`` describes a step executed
  at generation time.
* One ``Task`` is responsible for translating a specific set of elements in the input model to one
  output file in the output folder. The input set can be chosen arbitrarily, often this is the list
  of a certain model element type (e.g. instance of a ``Table`` class in a relational model from
  which SQL statements should be generated).

Using pymultigen means therefore to create one ``Generator`` class for your new generator and one or
more ``Task`` classes, one for each type of output artifact. If you are using a template-based code
generator under the hood, you usually will have one ``Task`` per output template.

Before you start, you need to check, whether pymultigen already has an integration for your
single-file code generator built-in. Currently, the following integrations are available:

* Jinja2

If you want to use another generation engine, you can easily add support yourself (the current
Jinja2 integration consists of less than 20 lines of code). If you've done so, please consider
giving back to the community. Your contribution is welcome! Please see below for instructions how to
extend pymultigen with a new integration.

Using the Jinja2 integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may want to check out `pyecoregen <https://github.com/pyecore/pyecoregen>`_, a code generator
from `pyecore <https://github.com/pyecore/pyecore>`_-based models to Python classes. It is a
concrete Jinja2-based code generator built with pymultigen.

Jinja2 is a template-based text generator. Writing a file-generator with Jinja therefore involves
writing a template for each type of output file. In pymultigen you will then implement a ``Task``
class per output file type, i.e. per Jinja template.

The general form of such a ``Task`` looks like this:

.. code-block:: python

    class MyTask(multigen.jinja.JinjaTask):

        # Name of template file used by this task.
        template_name = 'name-of-template.tpl'

        def filtered_elements(self, model):
            """Return iterator based over elements in model that are passed to template."""

        def relative_path_for_element(self, element):
            """Returns relative file path receiving the generator output for given element."""

The workflow engine will initially call ``filtered_elements``. This method is expected to return an
interator over model elements for which a single file needs to be generated. *Model* is meant here
in an abstract way: It may be an instance of a formal metamodel, but it could be any Python object,
like a dictionaries or lists. The contained elements being iterated over are accessible from within
a template as ``element``.

Once Jinja has produced a textual result it must be written to file. This is where
``relative_path_for_element`` comes into play. For a given element that was filtered from the model
before, it returns the corresponding filepath. Note that this path is interpreted to be relative to
the top-level output path of the overall generation (see below). If subfolders are mentioned here,
they are created on demand.

One of more tasks classes like this must then be registered with a top-level generator. Just like
before, a new ``Generator`` class is derived from the appropriate base class:

.. code-block:: python

    class MyGenerator(multigen.jinja.JinjaGenerator):

        # List of task objects to be processed by this generator.
        tasks = [
            MyTask(),
        ]

        # Root path where Jinja templates are found.
        templates_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'templates'
        )

        def create_environment(self, **kwargs):
            """Create Jinja2 environment."""
            environment = super().create_environment(**kwargs)
            # Do any customization of environment here, or delete this method.
            return environment

The base class implementation of {{create_environment}} passes {{templates_path}} to the created
environment object to allow Jinja to find the template names specified in a ``Tasks``'s
``template_name``. By overriding this method you can extend the environment, e.g. to add filters and
tests. Of course you can also completely replace the implementation, e.g. to change the way how
templates how looked up.

The example above simply instantiates the new ``Task`` class. Here you can optionally pass a
formatter function, that is then applied to the output of Jinja. Formatters are simple string
transformations, some of which are built-in in the ``formatters.py`` module. If you actually are
writing a Python code generator you may want to clean up the generated code according to pep8,
simply pass the appropriate formatter during task instantiation:

.. code-block:: python

    class MyGeneratorWithPep8(multigen.jinja.JinjaGenerator):

        # List of task objects to be processed by this generator.
        tasks = [
            MyTask(formatter=multigen.formatter.format_autopep8),
        ]

        ...

Extending pymultigen
--------------------

Contributions welcome!

Below the most typical extension scenarios are described. Note that in theory pymultigen can be used
with *any* code that produces text, not just a templating engine. Take a look at the class hierarchy
in ``generator.py`` to get more insights or drop me a note if this is something you plan to do.

Formatters
~~~~~~~~~~

Writing a new formatter is trivial: Simply create a function that transforms an input string into
the nicely formatted output string. If you want to get your formatter added to pymultigen, please
make sure that:

* New dependencies (like autopep8 in the existing pep8 formatter) are only imported in the
  formatting function. This way user only pay for what they use.
* Please write unittests and add your possible dependencies to the ``tests_require`` argument in
  ``setup.py``.

There is not much more to it.

Templating engine
~~~~~~~~~~~~~~~~~

For a live sample, look at the Jinja2 integration in ``jinja.py``. For your templating engine ``X``,
you probably have to write small ``Generator`` and ``Task`` base classes like this:

.. code-block:: python

    class XGenerator(TemplateGenerator):

        def __init__(self, environment=None, **kwargs):
            super().__init__(**kwargs)
            # Add any attributes to the generator that are static with respect to a full generation
            # run (over all files), like a Jinja2 environment.
            ...


    class XTask(TemplateFileTask):

        def generate_file(self, element, filepath):
            """Actual generation of element."""

Each element that is iterated over from the input model is eventually passed to the tasks's
``generate_file`` method. Here simply call you template engine to produce the output string. You
also want to apply the optional formatter before writing the string to disk. This is how the Jinja
task does it:

.. code-block:: python

    def generate_file(self, element, filepath):
        template = self.environment.get_template(self.template_name)
        context = self.create_template_context(element=element)

        with open(filepath, 'wt') as file:
            file.write(self.formatter(template.render(**context)))

The implementation shows two more things:

* The template to be used is retrieved from an ``environment`` that is specific to the template
  engine. Such an environment is usually passed down from the ``Generator`` class to the ``Task``.
* ``create_template_context`` is a function implemented in base class ``TemplateTask``. It
  implements the very common case of dictionaries being used as template context objects. Of course
  you can override this if it doesn't match your engine.
