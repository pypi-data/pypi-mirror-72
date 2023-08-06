=================
PyAMS_apm package
=================

Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp()

    >>> from pyams_apm.include import include_package as include_apm
    >>> include_apm(config)

    >>> from pyams_apm.tween import *

    >>> tearDown()
