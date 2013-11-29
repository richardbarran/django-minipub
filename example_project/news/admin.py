from django.contrib import admin

from mininews.admin import ArticleAdmin

from models import Article

class ArticleAdmin(ArticleAdmin):
    list_display = ('title', 'viewable', 'status', 'start')
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'body',)
        }),
        ArticleAdmin.PUBLICATION_FIELDSET,
        ArticleAdmin.SEO_FIELDSET,
        ArticleAdmin.TIMESTAMP_FIELDSET
    )

admin.site.register(Article, ArticleAdmin)
