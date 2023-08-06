========================
Django Google Translate
========================

Google Translate provides easy way to add google translate plugin in your django templates.
If your project needs to have multiple languages and if you dont want to manage .po files then you can add this package to make your website available in multiple languages easily without any hassle.

Quick start
-----------

1. Download the package::

    pip install django-google-translate

2. Load the translate tag in your template (ideally on base.html)::

    {% load google_translate %}

3. Add following template tag wherever you want to show translate button::

    {% google_translate %}
    