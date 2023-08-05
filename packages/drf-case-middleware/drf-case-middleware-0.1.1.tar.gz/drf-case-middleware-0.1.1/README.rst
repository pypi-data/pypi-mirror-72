====================================
DRF Case Middleware
====================================

Camel case to snake case and snake case to camel case for Django REST framework.

===============
Getting Started
===============

.. code-block:: bash

    $ pip install drf-case-middleware

Add the render and parser to your django settings file.

.. code-block:: python

    MIDDLEWARE = [
        # ... other middlewares
        'drf_case_middleware.middlewares.CaseMiddleware',
    ]

    REST_FRAMEWORK = {

        'DEFAULT_RENDERER_CLASSES': (
            'drf_case_middleware.renders.CaseJSONRenderer',
            'drf_case_middleware.renders.CaseBrowsableAPIRenderer',
            # ... other renderers
        ),

        'DEFAULT_PARSER_CLASSES': (
            'drf_case_middleware.parsers.CaseFormParser',
            'drf_case_middleware.parsers.CaseMultiPartParser',
            'drf_case_middleware.parsers.CaseJSONParser',
            # ... other renderers
        ),
    }

====
Note
====

This project is based on the `djangorestframework-camel-case <https://github.com/vbabiy/djangorestframework-camel-case>`_ project.

=======
License
=======

MIT License
