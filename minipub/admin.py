"""
We have a ``MinipubAdmin`` class that basically gives you the code for displaying 2
fieldsets:

#. The fieldset that controls publication:

.. image:: /img/minipub-fieldset.png

2. And the 'status' fieldset; these fields are read-only, and exist just for information:

.. image:: /img/minipub-status-fieldset.png

And here is an example of using them:

.. code-block:: python

    from minipub.admin import MinipubAdmin

    class ArticleAdmin(MinipubAdmin):

    # Other code...

    fieldsets = (
        (None, {
            'fields': ('some', 'other', 'fields',)
        }),
        MinipubAdmin.PUBLICATION_FIELDSET,
        MinipubAdmin.TIMESTAMP_FIELDSET
    )
"""
from django.contrib import admin


class MinipubAdmin(admin.ModelAdmin):

    readonly_fields = ('created', 'modified', 'status_changed')
    ordering = ['-start']

    TIMESTAMP_FIELDSET = ('Timestamps', {
        'description': 'When this record was created, last modified, and when '
        'the status was last changed.',
        'classes': ('collapse',),
        'fields': (('created', 'modified', 'status_changed'),)
    })

    PUBLICATION_FIELDSET = ('Publication', {
        'description': "You can control here the publication of this object.<br>"
        "An object is only 'live' if its status is 'published', <strong>and</strong> "
        "if today's date is after the start date. "
        "If the end date is entered, the object will no longer be live after that date.<br>"
        "<strong>Note:</strong> when you are logged in to the 'admin', you can preview "
        "this object in the website, even if it's not published.",
        'fields': (('status', 'start', 'end'),)
    })
