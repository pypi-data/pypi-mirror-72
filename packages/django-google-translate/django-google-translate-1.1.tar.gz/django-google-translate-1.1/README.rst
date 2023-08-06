========================
Django Google Translate
========================

Google Translate provides easy way to add google translate plugin in your django templates.
If your project needs to have multiple languages and if you dont want to manage .po files then you can add this package to make your website available in multiple languages easily without any hassle.

.. image:: https://i.ibb.co/TK59rCp/Annotation-2020-06-27-124837.jpg

| Simple

.. image:: https://i.ibb.co/pwC7SJn/Annotation-2020-06-27-124803.jpg

| Vertical

.. image:: https://i.ibb.co/YcxND7v/Annotation-2020-06-27-124821.jpg

| Horizontal


Quick start
-----------

1. Download the package::

    pip install django-google-translate

2. Add "google_translate" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'google_translate',
    ]

3. Load the translate tag in your template (ideally on base.html)::

    {% load google_translate %}

4. Add following template tag wherever you want to show translate button::

    {% google_translate %}

5. You can also pass type and default language in the translate button type in the inclusion tag (OPTIONAL)::

    {% google_translate type='vertical' language='en' %}

Available values for the type are "horizontal", "vertical" and "simple" (default) and for language you can pass any ISO language code
