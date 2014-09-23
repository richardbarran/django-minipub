from django.contrib import admin

from mininews.admin import MininewsAdmin

from .models import Article


class ArticleAdmin(MininewsAdmin):
    list_display = ('title', 'live', 'status', 'start')
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'body',)
        }),
        MininewsAdmin.PUBLICATION_FIELDSET,
        MininewsAdmin.TIMESTAMP_FIELDSET
    )

admin.site.register(Article, ArticleAdmin)
