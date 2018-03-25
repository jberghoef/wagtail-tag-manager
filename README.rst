Wagtail Tag Manager
===================

Disclaimer
----------

This package attempts to ease the implementation of tags by the new ePrivacy
rules as defined by the European Union. I urge you to read about these new rules
and ensure you are properly configuring your tags for both the analytical and
traceable variants. This package is free and the author can not be held
responsible for the correctness of your implementation, or the assumptions made
in this package to comply with the new ePrivacy regulation.

Read more about the `ePrivacy Regulation`_.

.. _ePrivacy Regulation: https://ec.europa.eu/digital-single-market/en/proposal-eprivacy-regulation

Requirements
------------

+---------+-----+
| Django  | 2.0 |
+---------+-----+
| Wagtail | 2.0 |
+---------+-----+

Instructions
------------

Installation::

    pip install wagtail-tag-manager

Add the application to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'wagtail.contrib.modeladmin',
        'wagtail_tag_manager',
        # ...
    ]

Include the middleware:

.. code-block:: python

    MIDDLEWARE = [
        # ...
        'wagtail_tag_manager.middleware.TagManagerMiddleware',
        # ...
    ]

Include the urls:

.. code-block:: python

    from django.urls import include, path
    from wagtail_tag_manager import urls as wtm_urls

    urlpatterns = [
        # ...
        path('wtm/', include(wtm_urls)),
        # ...
    ]


Concept
-------

+--------------------------------+------------+------------+-----------+
| State                          | Functional | Analytical | Traceable |
+--------------------------------+------------+------------+-----------+
| No cookies accepted.           | yes        | no         | no        |
+--------------------------------+------------+------------+-----------+
| Cookies implicitly accepted    | yes        | yes        | no        |
| through browser settings.      |            |            |           |
+--------------------------------+------------+------------+-----------+
| Cookies explicitly accepted,   | yes        | yes        | yes       |
| noting tracking functionality. |            |            |           |
+--------------------------------+------------+------------+-----------+

Note that in the case of analytical cookies or local storage, you are obliged to
still show a notification at least once, noting that you are using cookies for
analytical and performance measurement purposes.

When implementing tracking cookies, the user has to explicitly give permission
for you to enable them for their session. When asking for permission, you must
explicitly state the tracking functionality of the script you are using.

To ease the implementation by this concept, Wagtail Tag Manager allows you to
define a tag as functional, analytical of traceable. When properly configured,
it'll take care of loading the correct tag at the correct time, taking in
account the following scenario's:

**1. The user has not accepted cookies.**

+---------+------------+------------+-----------+
|         | Functional | Analytical | Traceable |
+---------+------------+------------+-----------+
| Instant | Yes        | No         | No        |
+---------+------------+------------+-----------+
| Lazy    | Yes        | No         | No        |
+---------+------------+------------+-----------+

**2. The user has accepted cookies through browser settings.**

+---------+------------+------------+-----------+
|         | Functional | Analytical | Traceable |
+---------+------------+------------+-----------+
| Instant | Yes        | Yes*       | No        |
+---------+------------+------------+-----------+
| Lazy    | Yes        | Yes        | No        |
+---------+------------+------------+-----------+

As the acceptance of analytical tags can only be verified client side, we'll
first load all the analytical tags lazy (whether they are instant or not).
On the next request we are able to instantly load the analytical tags marked as
'instant'.

Please note that we still have to show a message stating that we are using
analytical tags.

**3. The user has explicitly accepted tracking cookies for your site.**

+---------+------------+------------+-----------+
|         | Functional | Analytical | Traceable |
+---------+------------+------------+-----------+
| Instant | Yes        | Yes        | Yes*      |
+---------+------------+------------+-----------+
| Lazy    | Yes        | Yes        | Yes       |
+---------+------------+------------+-----------+

We'll load the traceable tags marked 'instant', after the user accepting the
usage of these tags, together with the lazy tags. On the next request we are
able to instantly load the traceable tags marked as 'instant'.
