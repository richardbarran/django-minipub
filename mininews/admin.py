from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    """Just some boilerplate code that is useful in child classes."""

    readonly_fields = ('created', 'modified', 'status_changed')
    ordering = ['-start']

    TIMESTAMP_FIELDSET = ('Timestamps', {
            'description': 'When this record was created, last modified, and when '
                'the status was last changed.',
            'classes': ('collapse',),
            'fields': (('created', 'modified', 'status_changed'),)
        })

    SEO_FIELDSET = ('SEO', {
            'description': "Meta elements provide information about the web page, "
            "which can be used by search engines to help categorize the page correctly.",
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_keywords', 'sitemap_priority')
    })

    PUBLICATION_FIELDSET = ('Publication', {
            'description': "You can control here the publication of this object.<br>"
                    "An object is only 'viewable' if its status is 'published', <strong>and</strong> "
                    "if today's date is after the start date. "
                    "If the end date is entered, the object will no longer be viewable after that date.<br>"
                    "<strong>Note:</strong> when you are logged in to the 'admin', you can preview "
                    "this object in the website, even if it's not published.",
            'fields': (('status', 'start', 'end'),)
    })


