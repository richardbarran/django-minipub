from django.contrib import admin

from minipub.admin import MinipubAdmin

from .models import Article


class ArticleAdmin(MinipubAdmin):
    list_display = ('title', 'live', 'status', 'start')
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'body',)
        }),
        MinipubAdmin.PUBLICATION_FIELDSET,
        MinipubAdmin.TIMESTAMP_FIELDSET
    )

admin.site.register(Article, ArticleAdmin)
