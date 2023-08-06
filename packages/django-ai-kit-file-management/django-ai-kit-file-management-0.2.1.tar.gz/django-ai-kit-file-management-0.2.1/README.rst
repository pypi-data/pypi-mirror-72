django-ai-kit-file-management
=============================================

django-ai-kit-file-management bundles everything related to
File-Management and is meant to
work seamlessly with the ai-kit-file-management react library.

Index
-----

* `Quick Start and Configuration`_

* `Api Documentation`_

* `Error Codes`_

Quick Start and Configuration
-----------------------------

1.) Add ``ai_kit_file_management`` to your ``INSTALLED_APPS`` like so:

::

    INSTALLED_APPS = (
        # ...
        "ai_kit_file_management",
    )
2.) Configuration is namespaced unter ``AI_KIT_FILE_MANAGMENT`` like so:

::

    AI_KIT_FILE_MANAGMENT = {
        "MAX_FILE_SIZE_KB": 2345,
        # ...
    }

Default configurations are:

::

    DEFAULTS = {
        # Which file model to use. This package has its own file model, but you
        # can inherit from `models.AbstractFile` to extend it and configure to
        # use it here.
        "FILE_MODEL": ai_kit_file_managment.models.File,
        # Same for the serializer
        "SERIALIZER": ai_kit_file_managment.serializers.FileSerializer,
        # The max file size that is allowed. Make sure front- and backend have
        # the same configuration for this!
        "MAX_FILE_SIZE_KB": 1000000,
        # File formats that can be uploaded as media types
        "ALLOWED_FORMATS": ai_kit_file_managment.settings.DEFAULT_FORMATS,
        # if you want to open the route to everyone, set PERMISSION_CLASSES to
        # (AllowAny,). For more specific access rules, define your own django
        # rest framework permission classes
        "PERMISSION_CLASSES": (IsAuthenticated,),
        # Possible fileserver backends are "dev", "nginx" and "x-sendfile"
        "FILESERVER_BACKEND": "dev",
    }

A note about ``ALLOWED_FORMATS``: ``DEFAULT_FORMATS`` is defined as:

::

    DEFAULT_FORMATS = [
        "image/jpeg",
        "image/png",
        "application/pdf",
        "application/zip",
        "text/comma-separated-values",
    ]

You can either define your own list or - if you only want to add a few formats -
import ``DEFAULT_FORMATS`` and extend it:

::

    from ai_kit_file_managment.settings import DEFAULT_FORMATS

    AI_KIT_FILE_MANAGMENT = {
        "ALLOWED_FORMATS": DEFAULT_FORMATS + ["text/plain"],
        # ...
    }

Ìf ``FILESERVER_BACKEND` is set to ``dev``, django will serve the file downloads.
This is recommended for production use and its better to use the X-Sendfile
feature to let the reverse proxy serve the actual files. This allowes django
to manage permissions, but let apache or nginx do the heavy lifting.

Set this configuration to ``nginx`` if you use nginx and ``x-sendfile`` if you
use Apache or (nearly) any other server. The demo project contains an example
configuration for nginx. Look into the demo settings
(``demo/backend/demo/settings.py``), into ``demo/docker-compose.yml``, the
Dockerfiles for backend and nginx and into the configuration file
``demo/nginx/django.conf`` to get an idea. We don't provide a detailed
explaination since the your production setup may differ.

3.) Include the routes in your ``urls.py``:

::

    urlpatterns = [
        # ...
        path("api/v1/file_management/", include("ai_kit_file_management.urls"))
        # ...
    ]

5.) Run ``python manage.py migrate``.


Api Documentation
=================

Of course you don't have to use the front and backend components in tandem.
But if you start to mix and match, you have to speak to the API directly.


Upload
------

This module provides a Multipart POST ``/upload/`` endpoint. The file to be
uploaded has to be set to the fieldname ``file``.

On successful creation of the file the response has the status code 201.

On error, it returns a 403 and

::

    {
        "file": [<error code 1>, <error code 2>, ...]
    }

Error Codes
^^^^^^^^^^^

The backend never sends user facing error messages, but general error codes.
Internationalisation happens in the frontend.

+---------------------------+--------------------------------------------------+
| error code                | possible user facing message                     |
+===========================+==================================================+
| `mime_type_not_allowed`   | Not allowed to upload file of this type          |
+---------------------------+--------------------------------------------------+
| `filename_too_long`       | The filename is too long                         |
+---------------------------+--------------------------------------------------+
| `filesize_too_large`      | The file is too large. Maximum allowed size is...|
+---------------------------+--------------------------------------------------+


Files
-----

In order to retrieve information about uploaded files, the backend provides the
``/files/`` endpoint for the list view of single files. It returns the
following json structure:

::
    [
        {
            "id": <database identifier of the file>,
            "file": <url, at which the file can actually be downloaded>,
            "creator": <id of user who created the file>,
            "format": <mime type or file type>,
            "name": <name of the file>
        },
        ...
    ]


Download
--------

The actual download of a file happens via the dedicated ``/download/<identifier>``
endpoint. The identifier is randomly generated and is not meant to be provided
manually. Rather, the url in ``"file"`` provided via ``/files/`` points to the
download endpoint and has the identifier integrated.

On success the backend returns a multipart response with the binary file data and
the following fields:

::
    {
        "filename": <name of the file>,
        "content_type": <mime type or file type>
    }

